# Spotify_ETL_Pipeline

problem statement: 
    we have a client who is passionate about music industry , and he wants to understand the music industry by collecting data and finding insights out of it. 
    He wants us to build an ETL [Extract, Transform, Load ] pipeline , where we'll be collecting the data on a weekly basis the top global songs from the spotify billboard using the spotify api [remember- the playlist updates on weekly basis], transform the data and store it in some storage location [s3 or DWH]. The client wants us to build a large dataset  so that after 1 or 2 year the he can perform the analysis and understand what type of songs are trending, who are the top artist, what kind of genre people love to listen, the pattern  or changes in the music industry based on listen's/users  music taste. 
   
Workflow:
![Screenshot (359)](https://github.com/Salvik24Bhowal/spotify_etl_project/assets/67736824/9caaafa3-2429-401e-a65f-0e39d06ebcbb)

1. we'll be using the spotify api and get the top global songs, [remember- the playlist updates on weekly basis] 
2. write python code for extraction,transformation,loading on local pc and then deploy it on aws lambda
3. useAWS Eventbridge(cloudwatch events) for scheduling daily trigger that will invoke the 'spotify_api_data_extract' lambda function, and run it per-min, 1x a day,week based on use case and it will store the extracted raw data in the form of json file in the 'to_be_processed' s3 sub-directory.
4. once the raw data is stored on s3, we will add another trigger(s3) that will call the  the lambda function to transform data and store the transformed data on s3 again.
5. once we got the transformed data, the glue crawler will run and it will go through each n every file on the s3 bucket and will fetch number of columns , column names, datatypes it has, etc. after that it will build a glue catalog that will have the information of the meta data like no. of columns, types of it.
6. Once we have the glue catalog , we can simply use the amazon athena to run sql queries on top of it for futher analysis.

Approach:
1. created a python file on local pc to test the ELT script. Explored the spotify api, cleaned the data, fetched necessary data, did some transformations and finally convert the data into DataFrame.
2. Deployed our ETL script on AWS cloud platform. Used lamda to do all the transformation, extraction and loading the data to storage location (s3).
3. Data extracted is stored in 'to_be_processed' sub-directory.
4. Nxt comes transformation where another lamda function is used to process and transform the data and move it into another sub-directory 'transformed_data' where there are 3 more sub-directory [album_data, song_data, artist_data] where after transforming the data into csv form is stored.
5. Also a copy of the 'to_be_processed' file is copied to 'rocessed' sub-directory after transformation, and its deleted from 'to_be_processed' directory. since we dont want to transform the same data again and again.
6. Nxt we have implemented trigger using aws cloudwatch where it will help us automate the entire ETL process, by extracting the raw data on timely basis[hourly,weekly,monthly] and s3 to invoke transformation trigger whenever the data is stored in 'to_be_processed' folder.
7. nxt we have used aws glue crawler to crawl through each and every transformed data and create a glue catalog, once its done we can run analytical queries on top of the data using athena directly from s3 bucket and perform our analysis and gain insigts out of it.
8. we could also implement visualisation tool like quicksight to find patterns and make informative and effective business decisions.
   

Tools and libraries:
1. jupyter notebook
2. spotipy lib for connecting spotify API & collecting spotify data
3. AWS Cloud Services [s3,lambda,athena,glue,cloudwatch]
