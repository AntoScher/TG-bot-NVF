from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="новости", callback_data="news"),
         InlineKeyboardButton(text="видео", callback_data="video"),
         InlineKeyboardButton(text="фото", callback_data="photo")]
    ])
    await message.answer(f'Привет {message.from_user.first_name}! Выбери категорию:', reply_markup=keyboard)

def register_handlers_start(dp: Dispatcher):
    dp.message.register(start, Command(commands=["start"]))
