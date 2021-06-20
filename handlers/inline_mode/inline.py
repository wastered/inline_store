from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link

from data.config import channel, ADMINS
from loader import dp
from utils.db_api import commands
from utils.misc import subscription


@dp.inline_handler(text='', state='*')
async def empty_query(query: types.InlineQuery):
    search = [
        types.InlineQueryResultArticle(
            id=shop.id, title=shop.name,
            input_message_content=types.InputTextMessageContent(
                message_text=f"Вы выбрали - <b>{shop.name}</b>\nЧтобы посмотреть полное описание товара,\n"
                             f"а так же его купить⤵️"
            ),
            thumb_url=shop.photo,
            description=f"Цена: {shop.price:,}₽",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Показать товар',
                        url=await get_start_link(f"{query.from_user.id}_{shop.id}")
                    )
                ]
            ]
            )
        )
        for shop in await commands.get_all_items()
    ]
    
    if await commands.select_user(query.from_user.id) or \
            await subscription.check(user_id=query.from_user.id, channel=channel) or \
            str(query.from_user.id) in ADMINS:
        await query.answer(results=search, cache_time=5, is_personal=True)
    
    else:
        await query.answer(results=search,
                           switch_pm_text="Бот не доступен. Подключить бота",
                           switch_pm_parameter=query.from_user.id,
                           cache_time=5,
                           is_personal=True
                           )


@dp.inline_handler(state='*')
async def some_query(query: types.InlineQuery):
    search = [
        types.InlineQueryResultArticle(
            id=shop.id, title=shop.name,
            input_message_content=types.InputTextMessageContent(
                message_text=f"Вы выбрали - <b>{shop.name}</b>\nЧтобы посмотреть полное описание товара,\n"
                             f"а так же его купить⤵️"
            ),
            thumb_url=shop.photo,
            description=f"Цена: {shop.price:,}₽",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Показать товар',
                        url=await get_start_link(f"{query.from_user.id}_{shop.id}")
                    )
                ]
            ]
            )
        )
        for shop in await commands.get_item(text=query.query)]
    
    if await commands.select_user(query.from_user.id) or \
            await subscription.check(user_id=query.from_user.id, channel=channel) or \
            str(query.from_user.id) in ADMINS:
        await query.answer(results=search,
                           cache_time=5,
                           is_personal=True)
    
    else:
        await query.answer(results=search,
                           switch_pm_text="Бот не доступен. Подключить бота",
                           switch_pm_parameter=query.from_user.id,
                           cache_time=5,
                           is_personal=True
                           )
