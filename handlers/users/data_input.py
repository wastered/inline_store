import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import hlink

from keyboards.default.location_contact import location_button, contact_button
from keyboards.inline.menu_keyboard import pay
from loader import dp
from utils.db_api.commands import get_item_id


@dp.callback_query_handler(text_contains='buy')
async def create_invoice(call: CallbackQuery, state: FSMContext):
    item_id = call.data.split(':')
    item_id = int(item_id[-1])
    item = await get_item_id(item_id)
    amount = float(item.price)
    photo = item.photo
    quantity_in_stock = (await get_item_id(item_id)).quantity
    
    await call.message.answer('Введите количество товара')
    await state.set_state('quantity_item')
    await state.update_data(item_id=item_id, item_name=item.name, amount=amount, quantity_in_stock=quantity_in_stock,
                            photo=photo)
    await call.answer(cache_time=60)


@dp.message_handler(state='quantity_item')
async def approve_payment_by_points(message: types.Message, state: FSMContext):
    try:
        answer = int(message.text)
    except ValueError:
        await message.answer("Введите число")
        return
    data = await state.get_data()
    
    if 0 < answer <= data['quantity_in_stock']:
        await message.answer('Отправьте контакт/напишите номер телефона в формате: \n'
                             '+79990147854\n'
                             '79990147854\n'
                             '8999829304',
                             reply_markup=contact_button)
        
        await state.set_state('contact')
        await state.update_data(quantity=answer, amount=data["amount"] * answer)
    
    else:
        await message.answer(f'Сейчас на складе {data["quantity_in_stock"]} ед. товара\n'
                             'Введите новое число', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Отмена', callback_data='cancel')
            ]
        ]))


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="contact")
async def get_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    
    await message.answer('Отправте геолокацию/напишите адрес доставки (город, улица, дом, подъезд, квартира)',
                         reply_markup=location_button)
    
    await state.update_data(contact=contact.phone_number)
    await state.set_state('delivery')


@dp.message_handler(text='Пропустить', state="contact")
async def skip_contact(message: types.Message, state: FSMContext):
    await message.answer('Отправте геолокацию/напишите адрес доставки (город, улица, дом, подъезд, квартира)',
                         reply_markup=location_button)
    
    await state.update_data(contact="-")
    await state.set_state('delivery')


@dp.message_handler(state="contact")
async def get_contact_text(message: types.Message, state: FSMContext):
    contact = message.text
    r = re.compile(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s/\.]?[0-9]{4,6}$")
    
    try:
        contact = r.match(contact).group()
    
    except AttributeError:
        await message.answer('Не правильный формат номера', reply_markup=contact_button)
        return
    
    await message.answer('Отправте геолокацию/напишите адрес доставки (город, улица, дом, подъезд, квартира)',
                         reply_markup=location_button)
    
    await state.update_data(contact=contact)
    await state.set_state('delivery')


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state="delivery")
async def get_location(message: types.Message, state: FSMContext):
    location = message.location
    location = f'http://maps.google.com/maps?q={location["latitude"]},{location["longitude"]}'
    data = await state.get_data()
    await message.answer_photo(data['photo'], reply_markup=ReplyKeyboardRemove())
    await message.answer('\n'.join([f'Вы приобретаете <b>{data["item_name"]}</b>\n',
                                    f'Количество товара <b>{data["quantity"]}</b>',
                                    hlink('Адрес доставки', url=location),
                                    f'Сумма к оплате <b>{data["amount"]:,}</b>₽\n']
                                   ), reply_markup=pay, disable_web_page_preview=True)
    
    await state.update_data(location=location)
    await state.set_state('payment method')


@dp.message_handler(state='delivery')
async def get_location_text(message: types.Message, state: FSMContext):
    location = message.text
    data = await state.get_data()
    await message.answer_photo(data['photo'], reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Вы приобретаете <b>{data["item_name"]}</b>\n'
                         f'Количество товара <b>{data["quantity"]}</b>\n'
                         f'Адрес доставки <b>{location}</b>\n'
                         f'Сумма к оплате <b>{data["amount"]:,}</b>₽\n', reply_markup=pay)
    
    await state.update_data(location=location)
    await state.set_state('payment method')
