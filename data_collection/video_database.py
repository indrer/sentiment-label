from googleapiclient.discovery import build
import json
import psycopg2
import video_collection
from secret import API_KEY, database_connect


SERVICE_NAME = 'youtube'
API_V = 'v3'
service = build(serviceName=SERVICE_NAME, version=API_V, developerKey=API_KEY)
print('Fetching youtube videos')
videos = video_collection.get_videos(service)
print('Connecting to the database')
connection = None
try:
    connection = psycopg2.connect(**database_connect) # hostname, database, username, password
    cur = connection.cursor()
    for video in videos:
        q = "insert into sentiment_anls.video values(%(url)s, %(title)s, %(upvote)s, %(downvote)s, %(views)s, %(commentCount)s, %(date)s) on conflict (url) do nothing"
        cur.execute(q, video)
    connection.commit()
    # close the communication with the PostgreSQL
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connection is not None:
        connection.close()
        print('Database connection closed.')
