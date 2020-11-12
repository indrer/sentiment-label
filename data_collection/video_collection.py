import random

def _parse_youtube_url(url):
    return url.replace('\n', '').split('/')[-1]

def _get_categories(service, region='US'):
    response = service.videoCategories().list(
        part='snippet',
        regionCode=region
    ).execute()
    category_list = []
    for item in response['items']:
        category_list.append(item['id'])
    return category_list

def get_videos_from_categories(service, region='US', cat_num=5, video_num=50):
    random_cat = random.sample(_get_categories(service, region), cat_num)
    # iterate over chosen categories and make requests for 
    # 50 videos with most views (trending), then 
    # randomly select 10 videos, get their ids, merge with get_manually_collected_video_ids
    # and return one array that should contain 100 videos if the default parameters are used
    # check for duplicates?


def get_manually_collected_video_ids():
    manually_collected_video_files = ['dislikedvideos.txt', 'middle.txt']
    manually_collected_video_ids = []
    # read manually collected videos
    for v in manually_collected_video_files:
        with open(v, 'r') as f:
            for line in f:
                manually_collected_video_ids.append(_parse_youtube_url(line))
    return manually_collected_video_ids
