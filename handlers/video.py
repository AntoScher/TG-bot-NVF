from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher  # Добавляем импорт Dispatcher
from api.video_api import search_videos

router = Router()

@router.message(lambda message: message.text == "Видео")
async def handle_video(message: types.Message):
    await message.answer("Введите ключевые слова для поиска видео:")

@router.message()
async def search_video(message: types.Message):
    query = message.text
    if not query:
        await message.answer("Пожалуйста, введите ключевые слова для поиска.")
        return
    videos = search_videos(query=query)
    if not videos:
        await message.answer("Видео не найдены.")
        return
    for video in videos:
        await message.answer(video)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться в меню"), KeyboardButton(text="Продолжить поиск")]
        ],
        resize_keyboard=True
    )
    await message.answer("Что дальше?", reply_markup=keyboard)

# Регистрируем обработчики
def register_handlers_video(dp: Dispatcher):
    dp.include_router(router)