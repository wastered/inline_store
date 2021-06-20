from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

invite = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Код приглашения")
        ],
        [
            KeyboardButton(text='Подписаться на канал')
        ],
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)
