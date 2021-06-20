from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import IP
from filters import IsAdmin
from loader import dp


@dp.message_handler(IsAdmin(), Command('admin'))
async def admin_django(message: types.Message):
    await message.answer('Перейти на сайт админки',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='💻', url=f'http://{IP}:8000/admin/')]
                         ]))
