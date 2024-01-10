# Spotify_ETL_Pipeline

problem statement: 
    we have a client who is passionate about music industry , and he wants to understand the music industry by collecting data and finding insights out of it. 
    He wants us to build an ETL [Extract, Transform, Load ] pipeline , where we'll be collecting the data on a weekly basis the top global songs from the spotify billboard using the spotify api [remember- the playlist updates on weekly basis], transform the data and store it in some storage location [s3 or DWH]. The client wants us to build a large dataset  so that after 1 or 2 year the he can perform the analysis and understand what type of songs are trending, who are the top artist, what kind of genre people love to listen, the pattern  or changes in the music industry based on listen's/users  music taste. 
   
Approach:
![Screenshot (359)](https://github.com/Salvik24Bhowal/spotify_etl_project/assets/67736824/9caaafa3-2429-401e-a65f-0e39d06ebcbb)

1. we'll be using the spotify api and get the top global songs, [remember- the playlist updates on weekly basis] 
2. write python code for extraction,transformation,loading and deploy on aws lambda
3. use amazon cloudwatch for scheduling triggers/events, ex- adding trigger that will call the lambda function to extract data from spotify on timely basis and load the raw data on s3.
4. once the raw data is stored on s3, we will add another trigger that will call the  the lambda function to transform data and store the transformed data on s3 again.
5. once we got the transformed data, the glue crawler will run and it will go through each n every file on the s3 bucket and will fetch number of columns , column names, datatypes it has .
6. after that it will build a glue catalog that will have the information of the meta data like no. of columns, types of it.
7. Once we have the glue catalog , we can simply use the amazon athena to run sql queries on top of it.

Tools and libraries:
1. jupyter notebook
2. spotipy lib for connecting spotify API & collecting spotify data
3. AWS Cloud Services [s3,lambda,athena,glue,cloudwatch]
