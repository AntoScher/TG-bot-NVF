import requests
from config import YOUTUBE_API_KEY

def get_video(query):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'q': query,
        'part': 'snippet',
        'maxResults': 5,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return ["Не удалось получить видео."]

    videos = []
    for item in data.get('items', []):
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        link = f'https://www.youtube.com/watch?v={video_id}'
        videos.append(f"{title}\n{link}")
    return videos
