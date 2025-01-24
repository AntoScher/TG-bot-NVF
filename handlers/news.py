import logging
from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from api.news_api import get_news

async def request_news(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введи текстовый запрос для новостей:")
    await state.set_state("awaiting_news_query")
    logging.info("Установлено состояние 'awaiting_news_query'.")

async def process_news_query(message: types.Message, state: FSMContext):
    logging.info(f"Получено текстовое сообщение: {message.text}")
    if await state.get_state() == "awaiting_news_query":
        query = message.text.strip()
        logging.info(f"Поисковый запрос: {query}")
        try:
            news_items = get_news(query)
            for item in news_items:
                await message.answer(item)
        except Exception as e:
            logging.error(f"Произошла ошибка при выполнении поиска: {e}")
            await message.answer(f"Произошла ошибка при выполнении поиска. Ошибка: {str(e)}")
        await state.clear()
        logging.info("Состояние сброшено.")

def register_handlers_news(dp: Dispatcher):
    dp.callback_query.register(request_news, lambda callback_query: callback_query.data == "news")
    dp.message.register(process_news_query)
