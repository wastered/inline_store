from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import get_start_link

from filters import Authentication
from keyboards.inline.menu_keyboard import buttons
from loader import dp
from utils.db_api import commands


@dp.message_handler(Authentication(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=buttons
                         )


@dp.callback_query_handler(text='deep_link')
async def get_deeplink(call: CallbackQuery):
    await call.message.answer(f"Ваша реферальная ссылка {await get_start_link(payload=call.from_user.id)}")
    await call.answer(cache_time=5)


@dp.callback_query_handler(text='point')
async def get_point(call: CallbackQuery):
    point = await commands.select_points(int(call.from_user.id))
    await call.message.answer(f"Ваши баллы: {point:.2f}")
    await call.answer(cache_time=5)


@dp.message_handler(Authentication(), Command('info'))
async def information(message: types.Message):
    await message.answer('Как получить "Баллы"?\n'
                         'Для начисления баллов поделитесь реферальной ссылкой, когда пользователь перейдет по ней, '
                         'Вы получите 10 баллов = 1000₽, которые можно потратить на покупку в магазине!\n'
                         'Получить реферальную ссылку, а так же посмотреть баллы можете по команде /start')
