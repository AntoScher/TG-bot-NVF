from aiogram import Router, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from api.photo_api import search_photos

router = Router()


# Обработчик для фото
@router.message(lambda message: message.text == "Фото")
async def handle_photo(message: types.Message):
    await message.answer("Введите ключевые слова для поиска фото:")


# Обработчик текстового запроса для фото
@router.message()
async def search_photo(message: types.Message):
    query = message.text
    photos = search_photos(query=query)

    if not photos:
        await message.answer("Фото не найдены.")
        return

    for photo_url in photos:
        await message.answer_photo(photo=photo_url)

    # Кнопки для продолжения или возврата в меню
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться в меню"), KeyboardButton(text="Продолжить поиск")]
        ],
        resize_keyboard=True
    )
    await message.answer("Что дальше?", reply_markup=keyboard)


# Регистрация обработчиков
def register_handlers_photo(dp: Dispatcher):
    dp.include_router(router)