from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink, hcode

from data import config
from keyboards.inline.menu_keyboard import paid_keyboard, discount
from loader import dp
from utils.db_api.commands import update_quantity, update_purchase, payment_point, select_points
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.callback_query_handler(text='yes', state='payment method')
@dp.callback_query_handler(text='no', state='payment method')
@dp.callback_query_handler(text='qiwi', state='payment method')
async def create_invoice(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    point = await select_points(int(call.from_user.id))
    point = float(point) * 100

    if call.data == 'qiwi' and point > 0:
        pay = data['amount'] - point if point <= data['amount'] / 2 else data['amount'] / 2
        await call.message.answer(f'✅<b>Ваши баллы {point/100}</b>\n'
                                  f'После списывания баллов сумма к оплате {pay:.2f}₽'
                                  f'\nЖелаете списать баллы?',
                                  reply_markup=discount)
        await call.answer(cache_time=30)
        return
    
    if call.data == 'yes':
        if point <= data['amount'] / 2:
            data['amount'],  point = data['amount'] - point, 0
            
        else:
            data['amount'], point = data['amount'] / 2, (point - data['amount'] / 2) / 100
            
        await state.update_data(amount=data['amount'], point=point, discount='yes')
    
    payment = Payment(amount=data['amount'])
    payment.create()
    
    await call.message.edit_text('\n'.join([f'Оплатите не менее: <b>{data["amount"]:,} ₽</b> по номеру телефона\n',
                                            hlink(config.WALLET_QIWI, url=payment.invoice),
                                            "И обязательно укажите ID платежа:",
                                            hcode(payment.id)]),
                                 reply_markup=paid_keyboard)
    
    await state.set_state('payment_qiwi')
    await state.update_data(payment=payment)
    await call.answer(cache_time=30)


@dp.callback_query_handler(text='cancel', state='*')
async def cancel_payment(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отменено")
    await state.finish()
    await call.answer(cache_time=30)


@dp.callback_query_handler(text='paid', state='payment_qiwi')
async def approve_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get('payment')
    
    try:
        payment.check_payment()
        
    except NoPaymentFound:
        await call.message.answer("Транзакция не найдена.")
        await call.answer(cache_time=10)
        return
    
    except NotEnoughMoney:
        await call.message.answer("Оплаченная сума меньше необходимой.")
        await call.answer(cache_time=10)
        return
    
    else:
        await call.message.answer("Успешно оплачено. Ожидайте доставку 📦")
        await update_quantity(data['item_id'], data['quantity'])
        await update_purchase(buyer=int(call.from_user.id), item_id=data['item_id'], amount=data['amount'],
                              quantity=data['quantity'], shipping_address=data['location'],
                              phone_number=data['contact'], successful=True)
        
        if data.get('discount', 'no') == 'yes':
            await payment_point(call.from_user.id, data['point'])

    await call.message.delete_reply_markup()
    await state.finish()
    await call.answer()
