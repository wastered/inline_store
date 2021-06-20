from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buttons = InlineKeyboardMarkup(
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(
                                           text="Получить реферальную ссылку",
                                           callback_data='deep_link'
                                       )
                                   ],
                                   [
                                       InlineKeyboardButton(
                                           text='Посмотреть кол-во баллов',
                                           callback_data='point'
                                       )
                                   ],
                                   [
                                       InlineKeyboardButton(
                                           text='Выбрать товар',
                                           switch_inline_query_current_chat=''
                                       )
                                   ]
                               ]
                               )

paid_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Оплатил", callback_data='paid')
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data='cancel')
        ]
    ]
)

discount = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='yes'),
            InlineKeyboardButton(text='Нет', callback_data='no')
        ]
    ]
)

pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Перейти к оплате', callback_data='qiwi')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)