import logging
from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация YouTube API клиента
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

async def request_video(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введи текстовый запрос для видео:")
    await state.set_state("awaiting_video_query")
    logging.info("Установлено состояние 'awaiting_video_query'.")

async def process_video_query(message: types.Message, state: FSMContext):
    logging.info(f"Получено текстовое сообщение: {message.text}")
    if await state.get_state() == "awaiting_video_query":
        query = message.text.strip()
        logging.info(f"Поисковый запрос: {query}")
        try:
            logging.info("Отправка запроса к YouTube API...")
            search_response = youtube.search().list(
                q=query,
                part="snippet",
                maxResults=1
            ).execute()
            logging.info("Запрос к YouTube API выполнен.")

            logging.info(f"Ответ API: {search_response}")

            if 'items' in search_response and search_response['items']:
                video_id = search_response['items'][0]['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_title = search_response['items'][0]['snippet']['title']
                await message.answer(f"**Название:** {video_title}\n**Ссылка:** {video_url}")
            else:
                await message.answer("Видео по вашему запросу не найдено.")
                logging.info("Видео по вашему запросу не найдено.")
        except Exception as e:
            logging.error(f"Произошла ошибка при выполнении поиска: {e}")
            await message.answer(f"Произошла ошибка при выполнении поиска. Ошибка: {str(e)}")
        await state.clear()
        logging.info("Состояние сброшено.")

def register_handlers_video(dp: Dispatcher):
    dp.callback_query.register(request_video, lambda callback_query: callback_query.data == "video")
    dp.message.register(process_video_query)
