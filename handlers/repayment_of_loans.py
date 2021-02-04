from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_REPAYMENT_OF_LOANS)
async def repayment_of_loans(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.payments(d))
            User().set_user_state(user_id, states.S_PAYMENTS)
        elif message.text == get_dict('repayment_of_loans_bank_type_hamkorbank', d):
            await bot.send_message(user_id, get_dict('repayment_of_loans_id', d), reply_markup=markups.cancel(d))
            User().set_user_state(user_id, states.S_REPAYMENT_OF_LOANS_HAMKORBANK)
        elif message.text == get_dict('repayment_of_loans_bank_type_other', d):
            await bot.send_message(user_id, get_dict('repayment_of_loans_id', d), reply_markup=markups.cancel(d))
            User().set_user_state(user_id, states.S_REPAYMENT_OF_LOANS_HAMKORBANK)
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/payments.py\nMethod: repayment_of_loans\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_REPAYMENT_OF_LOANS_HAMKORBANK)
async def repayment_of_loans_hamkorbank_id(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.repayment_of_loans_bank_type(d))
            User().set_user_state(user_id, states.S_REPAYMENT_OF_LOANS)
        elif str(message.text).isdecimal():
            await bot.send_message(user_id, get_dict('repayment_of_loans_password', d), reply_markup=markups.cancel(d))
            User().set_user_state(user_id, states.S_REPAYMENT_OF_LOANS_PASSWORD)
        else:
            await bot.send_message(user_id, get_dict('error_enter_amount_p2p', d))
            User().set_user_state(user_id, states.S_REPAYMENT_OF_LOANS_HAMKORBANK)
    except Exception as e:
        logger_app.error("/handlers/payments.py\nMethod: repayment_of_loans_hamkorbank_id\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_REPAYMENT_OF_LOANS_PASSWORD)
async def repayment_of_loans_hamkorbank_password(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        elif str(message.text).isdecimal():
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
    except Exception as e:
        logger_app.error("/handlers/payments.py\nMethod: repayment_of_loans_hamkorbank_password\n"+str(e))