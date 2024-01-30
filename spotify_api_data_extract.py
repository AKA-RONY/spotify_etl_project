import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client_id=os.environ.get('client_id')
    client_secret=os.environ.get('client_secret')
    
    #used for authentication [verifying creds]
    Client_Credential_Manager= SpotifyClientCredentials(client_id=client_id , client_secret=client_secret)
    #used for authorization [granting or denying access], creates an obj so that we can use the api to extract data from spotify
    sp= spotipy.Spotify(auth_manager=Client_Credential_Manager)
    playlists = sp.user_playlists('spotify')
    playlist_link="https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF"
    playlist_id= playlist_link.split('/')[-1] #breaks the string into list of substrings
    playlist_data=sp.playlist_tracks(playlist_id)
    # file_name= 'spotify_raw_data'+ str(datetime.now()) +'.json' #one way of writing the file name with extension

    client = boto3.client('s3')
    client.put_object(
        Bucket= 'spotify-etl-project-salvik',
        # Key= 'raw_data/to_be_processed/' +file_name, #one way of writing the file name with extension
        Key= 'raw_data/to_be_processed/spotify_raw_data ' + str(datetime.now()) +'.json',
        Body= json.dumps(playlist_data)
        )