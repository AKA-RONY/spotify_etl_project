import json
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO



#transformation logic for album data
def album(data):
    album_list=[]
    for item in data['items']:
    
        album_id =item['track']['album']['id']
        album_name=item['track']['album']['name']
        album_url=item['track']['album']['external_urls']['spotify']
        album_release_date=item['track']['album']['release_date']
        total_tracks=item['track']['album']['total_tracks']
        track_name= item['track']['name']
        song_url=item['track']['external_urls']['spotify']
        album_elements= {'album_id':album_id,'album_name':album_name,'album_url':album_url,"album_release_date":album_release_date,'album_tracks':total_tracks}
        album_list.append(album_elements)
    return album_list
    
#transformation logic for artist data    
def artist(data):
    artist_list=[]
    for item in data['items']:
        album_artist= item['track']['artists']
        for artist in album_artist:
            artist_id=artist['id']
            artist_name= artist['name']
            artist_url= artist['href']
            artist_elements={
                'artist_id':artist_id,'artist_name':artist_name,'artist_url':artist_url
            }
            artist_list.append(artist_elements)
    return artist_list

#transformation logic for songs data
def songs(data):
    song_list=[]
    for item in data['items']:
        song_id= item['track']['id']
        song_name= item['track']['name']
        song_duration_ms= item['track']['duration_ms']
        song_url= item['track']['external_urls']['spotify']
        song_popularity=item['track']['popularity']
        song_added= item['added_at']
        album_id= item['track']['album']['id']
        album_artist= item['track']['artists']
        
        artist_list=[]
        for artist in album_artist:
            artist_id=artist['id']
            artist_list.append(artist_id)
            
        song_element= { 
                        'song_id':song_id,
                       'song_name':song_name,
                       'song_duration [ms]':song_duration_ms,
                       'song_url':song_url,
                       'song_popularity':song_popularity,
                       'song_added':song_added,
                       'album_id':album_id,
                       'album_artist':artist_list
        }
        song_list.append(song_element)
        
    return song_list




def lambda_handler(event, context):
    s3= boto3.client('s3')
    Bucket='spotify-etl-project-salvik'
    key='raw_data/to_be_processed/'
    spotify_data=[]
    spotify_keys=[]
    
    
    #list all the files in the raw_data/to_be_processed folder
    # print(s3.list_objects(Bucket=Bucket, Prefix=key)['Contents'])
    
    for file in s3.list_objects(Bucket=Bucket, Prefix=key)['Contents']:
        file_key=file['Key']
        if file_key.split('.')[-1]=='json':
            response= s3.get_object(Bucket=Bucket,Key=file_key)
            content=response['Body']  
            JsonObject=json.loads(content.read())
            spotify_data.append(JsonObject)
            spotify_keys.append(file_key)
            
        
    for data in spotify_data:
        album_list= album(data)
        artist_list= artist(data)
        song_list= songs(data)
        

        album_df= pd.DataFrame.from_dict(album_list)
        album_df['album_release_date']=pd.to_datetime(album_df['album_release_date'])
        album_df=album_df.drop_duplicates(subset='album_id')
        

        artist_df= pd.DataFrame.from_dict(artist_list)
        artist_df= artist_df.drop_duplicates(subset='artist_id')
        
        
        song_df=pd.DataFrame.from_dict(song_list)
        song_df=song_df.drop_duplicates(subset='song_id')
        song_df['song_added'] = pd.to_datetime(song_df['song_added'])
      
        song_key= 'transformed_data/song_data/song_transformed ' + str(datetime.now()) + '.csv'
        song_buffer=StringIO() #converting song_df to string
        song_df.to_csv(song_buffer, index=False)
        song_content= song_buffer.getvalue()
        s3.put_object(Bucket=Bucket,Key=song_key,Body=song_content) # after transformation , the transformed data is moved to 'transformed_data' folder and a copy of transformed data is move to 'processed_data folder'. and the objects/data from 'to_be_processed folder ' is deleted after transoformation , since we dont want same data to be transformed again and again.

      
        artist_key= 'transformed_data/artist_data/artist_transformed ' + str(datetime.now()) + '.csv'
        artist_buffer=StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content= artist_buffer.getvalue()
        s3.put_object(Bucket=Bucket,Key=artist_key,Body=artist_content)
        
        
        # delimetter='|'
        album_key= 'transformed_data/album_data/album_transformed ' + str(datetime.now()) + '.csv'
        album_buffer=StringIO()
        # album_df.to_csv(album_buffer, index=False,sep=delimetter)
        album_df.to_csv(album_buffer, index=False)
        album_content= album_buffer.getvalue()
        s3.put_object(Bucket=Bucket,Key=album_key,Body=album_content)
        
    s3_resource= boto3.resource('s3')
    for key in spotify_keys:
        copy_source={
            'Bucket': Bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/processed/' + key.split("/")[-1])  # the extracted data when processed is copied from 'to_processed' to 'processed' folder
        s3_resource.Object(Bucket, key).delete() # and the data from to_be_processed folder is deleted , since we dont want to process the same data again and again. so it will delete the the file from 'to_be_processed' once its transformed and moved to 'processed' as well as 'transformed_folder'


        
        
       
   