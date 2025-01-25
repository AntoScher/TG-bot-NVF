import os
import requests
from typing import List, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_news(query: Optional[str] = None, from_date: Optional[str] = None) -> List[str]:
    """
    Получает новости по ключевым словам и дате.
    :param query: Ключевые слова для поиска.
    :param from_date: Дата в формате YYYY-MM-DD.
    :return: Список новостей.
    """
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': os.getenv('NEWS_API_KEY'),  # Используем переменную окружения
        'pageSize': 5,  # Ограничиваем количество новостей
        'q': query,  # Поиск по ключевым словам
        'from': from_date  # Фильтрация по дате
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        if data['status'] != 'ok' or not data['articles']:
            logger.warning("Новости не найдены или API вернул пустой ответ.")
            return ["Новости не найдены."]

        news = []
        for article in data['articles']:
            news.append(f"{article['title']}\n{article['url']}")

        return news

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к News API: {e}")
        return ["Не удалось получить новости. Пожалуйста, попробуйте позже."]