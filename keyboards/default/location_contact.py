from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

location_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="๐", request_location=True)
        ]
    ], resize_keyboard=True
)

contact_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="๐ฑ", request_contact=True),
            KeyboardButton(text='ะัะพะฟัััะธัั')
        ]
    ], resize_keyboard=True
)
