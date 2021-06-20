from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

location_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔍", request_location=True)
        ]
    ], resize_keyboard=True
)

contact_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱", request_contact=True),
            KeyboardButton(text='Пропустить')
        ]
    ], resize_keyboard=True
)
