import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Токен Telegram бота
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Ключи API для новостей, фото и видео
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Настройки базы данных SQLite
# DATABASE_URL = "sqlite:///database.db"