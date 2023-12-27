from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Змінити клас")
    ]
], resize_keyboard=True)