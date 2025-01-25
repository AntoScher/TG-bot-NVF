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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация всех обработчиков
def register_all_handlers(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_news(dp)
    register_handlers_video(dp)
    register_handlers_photo(dp)

async def main():
    logging.info("Запуск бота...")
    register_all_handlers(dp)  # Регистрируем все обработчики
    await dp.start_polling(bot)
    logging.info("Бот остановлен.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")