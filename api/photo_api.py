import requests
from config import UNSPLASH_ACCESS_KEY

def get_photo(query):
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': query,
        'per_page': 5,
        'client_id': UNSPLASH_ACCESS_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return ["Не удалось получить фотографии."]

    photos = []
    for item in data.get('results', []):
        photo_url = item['urls']['regular']
        photos.append(photo_url)
    return photos
