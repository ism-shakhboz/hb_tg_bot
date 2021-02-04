from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_PAYMENTS)
async def payments(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        elif message.text == get_dict('card_to_card_transfers', d):
            await bot.send_message(user_id, get_dict('enter_card_number', d), reply_markup=markups.cancel(d))
            User().set_user_state(user_id, states.S_CARD_TO_CARD)
        elif message.text == get_dict('repayment_of_loans', d):
            await bot.send_message(user_id, get_dict('developing', d))
            #await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.repayment_of_loans_bank_type(d))
            #User().set_user_state(user_id, states.S_REPAYMENT_OF_LOANS)
        elif message.text == get_dict('mobile_operators', d):
            await bot.send_message(user_id, get_dict('payment_mobile_operators', d), reply_markup=markups.payment_mobile_operators(user_id, d))
            User().set_user_state(user_id, states.S_PAYMENT_MOBILE_OPERATORS)
        else:
            await bot.send_message(user_id, get_dict('payments_hint', d))
    except Exception as e:
        logger_app.error("/handlers/payments.py\nMethod: payments\n"+str(e))
