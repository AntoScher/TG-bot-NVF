from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Обработчик команды /start
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Новости", callback_data="news"),
            InlineKeyboardButton(text="Видео", callback_data="video"),
            InlineKeyboardButton(text="Фото", callback_data="photo")
        ]
    ])
    await message.answer(
        f"Привет, {message.from_user.first_name}! Выбери категорию:",
        reply_markup=keyboard
    )

# Обработчик для inline-кнопок
async def handle_category_callback(callback: types.CallbackQuery):
    category = callback.data
    await callback.answer(f"Вы выбрали: {category}")
    await callback.message.answer(f"Вы выбрали категорию: {category}. Введите запрос для поиска.")

# Регистрация обработчиков
def register_handlers_start(dp: Dispatcher):
    dp.message.register(start, Command(commands=["start"]))
    dp.callback_query.register(handle_category_callback, lambda c: c.data in ["news", "video", "photo"])