import psycopg2
from secret import API_KEY, database_connect
from googleapiclient.discovery import build
import os.path
import numpy as np
from csv import writer
from datetime import datetime

connection = None
video_ids = []
comments = []
SERVICE_NAME = 'youtube'
API_V = 'v3'
service = build(serviceName=SERVICE_NAME, version=API_V, developerKey=API_KEY)
video_file = 'secret_videolist.txt'
nextToken = None
with open('secret_nextpagetoken.txt', 'a+') as f:
    if f.read().splitlines():
        lines = f.read().splitlines()
        nextToken = lines[-1].replace('\n', '')

def send_request(token):
    if (token is not None) and (len(token) > 0):
        return service.commentThreads().list(
                    part='snippet',
                    maxResults=100,
                    order='time',
                    textFormat='plainText',
                    videoId=videoid,
                    pageToken=token
                ).execute()
    else:
        return service.commentThreads().list(
            part='snippet',
            maxResults=100,
            order='time',
            textFormat='plainText',
            videoId=videoid,
        ).execute()

def put_comment_in_dict(item, videoid):
    comment = {}
    comment['body'] = item['snippet']['topLevelComment']['snippet']['textOriginal']
    comment['positive'] = 0
    comment['negative'] = 0
    comment['neutral'] = 0
    comment['rated'] = 0
    comment['comment_id'] = item['snippet']['topLevelComment']['id']
    comment['video_id'] = videoid
    comment['date'] = item['snippet']['topLevelComment']['snippet']['updatedAt']
    return comment

try:
    connection = psycopg2.connect(**database_connect) # hostname, database, username, password
    connection.autocommit = True
    cur = connection.cursor()

    if not os.path.isfile(video_file):
        print('File doesn\'t exist, fetching videos from the database')
        query = 'select * from sentiment_anls.video'
        cur.execute(query)
        videos = cur.fetchall()
        with open ('secret_videolist.txt', 'w') as f:
            for video in videos:
                video_ids.append(video[0])
                print(video[0], file=f)
    
    comments = []
    if len(video_ids) == 0:
        try:
            with open(video_file, 'r') as f:
                for line in f:
                    video_ids.append(line)
        except Exception as error:
            print(error)

    while len(video_ids) > 0:
        videoid = video_ids.pop().replace('\n', '')
        print('Reading video id ', str(videoid))
        response = send_request(nextToken)
        comment_count = 5000
        while response and comment_count > 0:
            for item in response['items']:
                comment = put_comment_in_dict(item, videoid)
                comments.append(comment)
            comment_count = comment_count - 100 # max per response
            if 'nextPageToken' in response:
                with open('secret_nextpagetoken.txt', 'a+') as f:
                    f.write(response['nextPageToken'])
                    f.write('\n')
                response = send_request(response['nextPageToken'])
            else:
                nextToken = None
                break
        with open(str(datetime.date(datetime.now()))+'.csv', 'w', encoding='utf8') as f:
            csv_writer = writer(f)
            for c in comments:
                csv_writer.writerow([c['body'], c['positive'], c['negative'], c['neutral'], c['rated'], c['comment_id'], c['video_id'], c['date']])
        with open ('secret_videolist.txt', 'w') as f:
            for video in video_ids:
                f.write("%s" % video)
    # np.random.shuffle(comments)
    # q = 'insert into sentiment_anls.comment values(%(body)s, %(positive)s, %(negative)s, %(neutral)s, %(rated)s, %(comment_id)s, %(video_id)s, %(date)s) on conflict (comment_id) do nothing'
    # for c in comments:
    #     cur.execute(q, c)

    # close the communication with the PostgreSQL
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connection is not None:
        connection.close()
        print('Database connection closed.')


