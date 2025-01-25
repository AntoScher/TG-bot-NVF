from aiogram import Router, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from api.video_api import search_videos

router = Router()


# Обработчик для видео
@router.message(lambda message: message.text == "Видео")
async def handle_video(message: types.Message):
    await message.answer("Введите ключевые слова для поиска видео:")


# Обработчик текстового запроса для видео
@router.message()
async def search_video(message: types.Message):
    query = message.text
    videos = search_videos(query=query)

    if not videos:
        await message.answer("Видео не найдены.")
        return

    for video in videos:
        await message.answer(video)

    # Кнопки для продолжения или возврата в меню
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться в меню"), KeyboardButton(text="Продолжить поиск")]
        ],
        resize_keyboard=True
    )
    await message.answer("Что дальше?", reply_markup=keyboard)


# Регистрация обработчиков
def register_handlers_video(dp: Dispatcher):
    dp.include_router(router)