import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink

from data.config import channel, ADMINS
from filters import WithoutAuthorization, Authentication
from keyboards.default import get_access
from keyboards.inline.menu_keyboard import buttons
from loader import dp, bot
from utils.db_api import commands
from utils.misc import subscription


@dp.message_handler(Authentication(), CommandStart(deep_link=re.compile('[0-9_]+')))
async def connect_user(message: types.Message, item_id=0):
    arg = message.get_args().split('_')[1] if item_id == 0 else item_id
    item = await commands.get_item_id(arg)

    if item.quantity > 0:
        await message.answer_photo(photo=item.photo, caption=f"<b>{item.name}</b>\n"
                                                             f"<b>В наличии</b> - {item.quantity} шт.\n"
                                                             f"<b>Цена</b> - {item.price:,}₽\n\n"
                                                             f"{item.description}",
                                   reply_markup=InlineKeyboardMarkup(
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text='Купить',
                                                   callback_data=f"buy:{item.id}"
                                               )
                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text='Поделиться', switch_inline_query=item.name
                                               )
                                           ]
                                       ]
                                   ))


@dp.message_handler(CommandStart(deep_link=re.compile('[\w\W]+')))
async def ref_start(message: types.Message):
    referrer = message.get_args().split('_')
    
    # для людей которые перешли через инлайн мод
    if int(referrer[0]) == message.from_user.id:
        if await subscription.check(user_id=message.from_user.id, channel=channel) or \
                str(message.from_user.id) in ADMINS:
            await commands.add_user(user_id=message.from_user.id,
                                    full_name=message.from_user.full_name,
                                    username=message.from_user.username)
            if len(referrer) > 1:
                await connect_user(message)
            else:
                await message.answer(f"Привет {message.from_user.full_name}.\n Ты был авторизован!🥳 \n"
                                     "Про начисление баллов вы можете прочитать нажав на команду /info",
                                     reply_markup=buttons)
        
        else:
            if len(referrer) > 1:
                await commands.storage_item(message.from_user.id, referrer[1])
            await empty_start(message)
    
    # для людей которые перешли по диплинку друга
    elif await commands.select_user(int(referrer[0])):
        await commands.add_user(user_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
        await commands.add_referrer(referrer_id=referrer[0], user_id=message.from_user.id)
        await commands.update_point(user_id=referrer[0])
        
        await message.answer(
            f'Привет, {message.from_user.full_name}! \n'
            f'Ты был авторизован!🥳 \n'
            f'Про начисление баллов вы можете прочитать нажав на команду /info', reply_markup=buttons)
        
        if len(referrer) > 1:
            await connect_user(message)
    else:
        await message.answer("Нерабочая DeepLink ссылка!\n"
                             "Попробуйте еще раз с актуальной ссылкой или нажмите /start")


@dp.message_handler(WithoutAuthorization(), CommandStart())
async def empty_start(message: types.Message):
    if await subscription.check(user_id=message.from_user.id, channel=channel):
        await commands.add_user(user_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             'Про начисление баллов вы можете прочитать нажав на команду /info', reply_markup=buttons)
        return
    
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Чтобы использовать этого бота введите код приглашения, либо пройдите по реферальной ссылке."
                         f"\nЕсли у вас нет  приглашения, то вы можете подписаться на канал.\n",
                         reply_markup=get_access.invite
                         )


@dp.message_handler(text='Отмена', state='*')
async def cancel_button(message: types.Message, state):
    link = await bot.export_chat_invite_link(chat_id=channel)
    await message.answer(text=f"Чтобы получить доступ выполните одно из этих действий:\n"
                              f"▪️перейдите по реферальной ссылке\n"
                              f"▪️подпишитесь на {hlink('канал', url=link)}\n"
                              f"▪️введите код приглашения",
                         reply_markup=get_access.invite)
    await state.finish()


@dp.message_handler(text="Код приглашения", state=None)
async def give_invite(message: types.Message, state: FSMContext):
    await message.answer('Пришлите свой код приглашения',
                         reply_markup=get_access.cancel)
    
    await state.set_state('code')


@dp.message_handler(state='code')
async def state_code(message: types.Message, state: FSMContext):
    answer = message.text
    
    if await commands.get_code(answer) is not None:
        await commands.add_user(user_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
        
        await message.answer("Поздравляю🎉\nВы прошли авторизацию!",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer('Про начисление баллов вы можете прочитать нажав на команду /info', reply_markup=buttons)
        await state.finish()
        try:
            item_id = await commands.get_storage_item(message.from_user.id)
            await commands.delete_storage_item(message.from_user.id)

            await connect_user(message, item_id)
        except AttributeError:
            return
    
    else:
        await message.answer(f'Не правильный код приглашения\n'
                             f'Попробуйте снова или нажмите кнопку Cancel',
                             reply_markup=get_access.cancel)


@dp.message_handler(text="Подписаться на канал", state=None)
async def give_invite(message: types.Message, state: FSMContext):
    link = await bot.export_chat_invite_link(chat_id=channel)
    await message.answer(f'Подпишитесь на {hlink("канал", url=link)}\n'
                         f'После этого нажмите /start\n'
                         f'Чтобы вернутся обратно нажмите Cancel',
                         reply_markup=get_access.cancel)
    
    await state.set_state('channel')


@dp.message_handler(state='channel')
async def state_channel(message: types.Message, state: FSMContext):
    if await subscription.check(user_id=message.from_user.id, channel=channel) or \
                str(message.from_user.id) in ADMINS:
        await commands.add_user(user_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
        
        await message.answer('Поздравляю🎉\nВы прошли авторизацию!', reply_markup=ReplyKeyboardRemove())
        await message.answer('Про начисление баллов вы можете прочитать нажав на команду /info', reply_markup=buttons)
        await state.finish()
        
        try:
            item_id = await commands.get_storage_item(message.from_user.id)
            await commands.delete_storage_item(message.from_user.id)

            await connect_user(message, item_id)
        except AttributeError:
            return
    else:
        link = await bot.export_chat_invite_link(chat_id=channel)
        await message.answer("Вы не подписались на канал.\n"
                             f'{hlink("Попробуйте снова", url=link)}\n'
                             f"или нажмите кнопку Отмена",
                             reply_markup=get_access.cancel)
