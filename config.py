import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
API_KEY_NEWS = os.getenv('API_KEY_NEWS')
OW_API_KEY= os.getenv('OW_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
