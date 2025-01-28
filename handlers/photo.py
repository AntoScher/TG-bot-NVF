from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher  # Добавляем импорт Dispatcher
from api.photo_api import search_photos

router = Router()

@router.message(lambda message: message.text == "Фото")
async def handle_photo(message: types.Message):
    await message.answer("Введите ключевые слова для поиска фото:")

@router.message()
async def search_photo(message: types.Message):
    query = message.text
    if not query:
        await message.answer("Пожалуйста, введите ключевые слова для поиска.")
        return
    photos = search_photos(query=query)
    if not photos:
        await message.answer("Фото не найдены.")
        return
    for photo_url in photos:
        await message.answer_photo(photo=photo_url)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться в меню"), KeyboardButton(text="Продолжить поиск")]
        ],
        resize_keyboard=True
    )
    await message.answer("Что дальше?", reply_markup=keyboard)

# Регистрируем обработчики
def register_handlers_photo(dp: Dispatcher):
    dp.include_router(router)