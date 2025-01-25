from aiogram import Router, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from api.news_api import get_news

router = Router()


# Обработчик для новостей
@router.message(lambda message: message.text == "Новости")
async def handle_news(message: types.Message):
    await message.answer("Введите ключевые слова для поиска новостей:")


# Обработчик текстового запроса для новостей
@router.message()
async def search_news(message: types.Message):
    query = message.text
    news = get_news(query=query)

    if not news:
        await message.answer("Новости не найдены.")
        return

    for item in news:
        await message.answer(item)

    # Кнопки для продолжения или возврата в меню
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться в меню"), KeyboardButton(text="Продолжить поиск")]
        ],
        resize_keyboard=True
    )
    await message.answer("Что дальше?", reply_markup=keyboard)


# Регистрация обработчиков
def register_handlers_news(dp: Dispatcher):
    dp.include_router(router)