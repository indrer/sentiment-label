from googleapiclient.discovery import build
import json
import psycopg2
from secret import API_KEY, database_connect

print('Connecting to the database')
connection = None
try:
    connection = psycopg2.connect(**database_connect)

    cur = connection.cursor()
	# execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    db_version = cur.fetchone()
    print(db_version)
       
	# close the communication with the PostgreSQL
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connection is not None:
        connection.close()
        print('Database connection closed.')

SERVICE_NAME = 'youtube'
API_V = 'v3'


service = build(serviceName=SERVICE_NAME, version=API_V, developerKey=API_KEY)

def get_videos_by_viewcount(video_num=50, query='trailer'):
    if video_num > 50 or video_num < 0:
        print('Make sure video number is between numbers 0 and 50!')
        return None
    
    response = service.search().list(
        part='snippet',
        maxResults=video_num,
        order='viewCount',
        q=query,
        relevanceLanguage='en',
        type='video').execute()
    return response
