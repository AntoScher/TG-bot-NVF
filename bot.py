import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_API_TOKEN
from handlers.start import register_handlers_start
from handlers.news import register_handlers_news
from handlers.video import register_handlers_video
from handlers.photo import register_handlers_photo

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

register_handlers_start(dp)
register_handlers_news(dp)
register_handlers_video(dp)
register_handlers_photo(dp)

async def main():
    logging.info("Запуск бота.")
    await dp.start_polling(bot)
    logging.info("Бот остановлен.")

if __name__ == '__main__':
    logging.info("Запуск основного скрипта.")
    asyncio.run(main())
    logging.info("Основной скрипт завершен.")
