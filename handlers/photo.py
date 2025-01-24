import os
import logging
import requests
from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import urlparse, unquote
from config import UNSPLASH_ACCESS_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

photo_urls = {}


def get_action_keyboard(sent_message_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Загрузить фото", callback_data=f"upload_photo|{sent_message_id}")],
            [InlineKeyboardButton(text="Продолжить поиск", callback_data="continue_search")]
        ]
    )
    return keyboard


async def request_photo(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введи текстовый запрос для фото:")
    await state.set_state("awaiting_photo_query")
    logging.info("Установлено состояние 'awaiting_photo_query'.")


async def process_photo_query(message: types.Message, state: FSMContext):
    logging.info(f"Получено текстовое сообщение: {message.text}")
    if await state.get_state() == "awaiting_photo_query":
        query = message.text.strip()
        logging.info(f"Поисковый запрос: {query}")
        try:
            logging.info("Отправка запроса к Unsplash API...")
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
            params = {"query": query, "per_page": 3}
            response = requests.get(url, headers=headers, params=params)
            logging.info("Запрос к Unsplash API выполнен.")

            data = response.json()
            logging.info(f"Ответ API: {data}")

            if data["total"] == 0:
                await message.answer("Не найдено подходящих фото. Пожалуйста, уточните запрос.")
                await state.clear()
                logging.info("Состояние сброшено.")
                return

            for photo in data["results"]:
                photo_url = photo["urls"]["regular"]
                sent_message = await message.answer_photo(photo=photo_url, caption="Подходит это фото?",
                                                          reply_markup=get_action_keyboard(photo["id"]))
                photo_urls[photo["id"]] = photo_url
            await message.answer("Если нужно уточнить запрос, напишите его заново.")
            await state.clear()
            logging.info("Состояние сброшено.")
        except Exception as e:
            logging.error(f"Произошла ошибка при выполнении поиска: {e}")
            await message.answer(f"Произошла ошибка при выполнении поиска. Ошибка: {str(e)}")


async def handle_callbacks(query: types.CallbackQuery):
    callback_data = query.data

    if callback_data.startswith("upload_photo"):
        photo_id = callback_data.split("|")[1]
        photo_url = photo_urls.get(photo_id)
        logging.info(f"Получаем URL фото для photo_id: {photo_id} -> {photo_url}")

        if photo_url:
            await bot.send_message(query.message.chat.id, "Фото будет загружено на сервер в папку img.")
            response = requests.get(photo_url)
            if response.status_code == 200:
                parsed_url = urlparse(photo_url)
                file_name = os.path.basename(parsed_url.path)
                file_name = unquote(file_name)
                file_path = os.path.join('img', file_name)
                if not file_path.endswith('.jpg'):
                    file_path += '.jpg'
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                await bot.send_message(query.message.chat.id, f"Фото загружено как {file_path}")
            else:
                await bot.send_message(query.message.chat.id, "Не удалось загрузить фото.")
        else:
            await bot.send_message(query.message.chat.id, "Не удалось найти фото для загрузки.")
    elif callback_data == "continue_search":
        await bot.send_message(query.message.chat.id, "Пожалуйста, напишите новый поисковый запрос.")


def register_handlers_photo(dp: Dispatcher):
    dp.callback_query.register(request_photo, lambda callback_query: callback_query.data == "photo")
    dp.message.register(process_photo_query)
    dp.callback_query.register(handle_callbacks)
