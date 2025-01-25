import os
import requests
from typing import List
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_videos(query: str, max_results: int = 3) -> List[str]:
    """
    Ищет видео на YouTube по ключевым словам.
    :param query: Ключевые слова для поиска.
    :param max_results: Максимальное количество результатов.
    :return: Список ссылок на видео.
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': os.getenv('YOUTUBE_API_KEY'),
        'part': 'snippet',
        'q': query,
        'maxResults': max_results,
        'type': 'video'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        if not data.get('items'):
            logger.warning("Видео не найдены.")
            return ["Видео по вашему запросу не найдены."]

        videos = []
        for item in data['items']:
            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(video_url)

        return videos

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к YouTube API: {e}")
        return ["Не удалось получить видео. Пожалуйста, попробуйте позже."]