import os
import requests
from typing import List
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_photos(query: str, max_results: int = 3) -> List[str]:
    """
    Ищет фото на Unsplash по ключевым словам.
    :param query: Ключевые слова для поиска.
    :param max_results: Максимальное количество результатов.
    :return: Список URL фотографий.
    """
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {os.getenv('UNSPLASH_API_KEY')}"}
    params = {"query": query, "per_page": max_results}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        if data["total"] == 0:
            logger.warning("Фото не найдены.")
            return ["Фото по вашему запросу не найдены."]

        photos = []
        for photo in data["results"]:
            photos.append(photo["urls"]["regular"])

        return photos

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к Unsplash API: {e}")
        return ["Не удалось получить фото. Пожалуйста, попробуйте позже."]