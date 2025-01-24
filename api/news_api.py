import requests
from config import API_KEY_NEWS


def get_news(query):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': API_KEY_NEWS,
        'pageSize': 5
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return ["Не удалось получить новости."]

    news = []
    for article in data.get('articles', []):
        title = article.get('title', 'Без названия')
        link = article.get('url', '')
        news.append(f"{title}\n{link}")
    return news
