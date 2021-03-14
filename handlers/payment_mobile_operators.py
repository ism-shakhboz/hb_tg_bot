from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from cryptography.fernet import Fernet
import datetime as dt
import api
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database_connection.dbcon import *

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_PAYMENT_MOBILE_OPERATORS'))
async def mobile_operators(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
        elif (str(message.text).startswith('+998') and len(str(message.text)) == 13) or (
                str(message.text).startswith('998') and len(str(message.text)) == 12):
            mobile_payment_report_commit(user_id, first_name, last_name, str(message.text).replace('+', ''), str(dt.datetime.now()))
            set_mobile_payment_oper_id_app_user(user_id, (get_mobile_payment_oper_id(user_id)[0]))
            set_user_state(user_id, get_state_by_key('S_TYPE_SUM_MOBILE_PAYMENT'))
            await bot.send_message(user_id, get_dict('enter_amount', d), reply_markup=markups.cancel(d))
        elif (str(message.text).startswith('9') and len(str(message.text)) == 9) or \
                (str(message.text).startswith('8') and len(str(message.text)) == 9):
            mobile_payment_report_commit(user_id, first_name, last_name, '998'+str(message.text), str(dt.datetime.now()))
            set_mobile_payment_oper_id_app_user(user_id, (get_mobile_payment_oper_id(user_id)[0]))
            set_user_state(user_id, get_state_by_key('S_TYPE_SUM_MOBILE_PAYMENT'))
            await bot.send_message(user_id, get_dict('enter_amount', d), reply_markup=markups.cancel(d))
        else:
            await bot.send_message(user_id, get_dict('phone_number_error', d), reply_markup=markups.payment_mobile_operators(user_id, d))
            set_user_state(user_id, get_state_by_key('S_PAYMENT_MOBILE_OPERATORS'))
    except Exception as e:
        logger_app.error("/handlers/payments.py\nMethod: mobile_operators\n" + str(e))

def load_key():
    return open("secretCardDecodeKey.key", "rb").read()

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_TYPE_SUM_MOBILE_PAYMENT'))
async def enter_amount(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if str(message.text).isnumeric():
            if float(message.text)<500:
                await bot.send_message(user_id, get_dict('minimum_sum_mobile_payment', d))
                set_user_state(user_id, get_state_by_key('S_TYPE_SUM_MOBILE_PAYMENT'))
            else:
                set_mobile_payment_amount((get_mobile_payment_oper_id(user_id)[0]), float(str(message.text)))
                res = get_dict('choose_card', d)
                rows = get_all_cards(user_id)
                cards_inline = InlineKeyboardMarkup()
                if len(rows) > 0:
                    for row in rows:
                        cards_inline.add(InlineKeyboardButton(row[0] + ' ' + row[1], callback_data="mp" + row[0]))
                    await bot.send_message(user_id, res, reply_markup=cards_inline)
                else:
                    await bot.send_message(user_id, get_dict('card_check', d))   
        elif message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
        else:
            await bot.send_message(user_id, get_dict('error_enter_amount_p2p', d), reply_markup=markups.cancel(d))
    except Exception as e:
        logger_app.error("/handlers/money_transfer.py\nMethod: enter_amount\n" + str(e))

@dp.callback_query_handler(lambda c: c.data.find("mp") > -1)
async def mp(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        d = get_lang(user_id)
        key = load_key()
        f = Fernet(key)
        
        encoded_card = get_card_encode(user_id, callback_query.data[2:])
        decrypted_card = f.decrypt(bytes((encoded_card[0])[2:-1], encoding='utf8'))
        balance = api.getCardBalance(decrypted_card.decode(), encoded_card[1])
        
        set_mobile_payment_from_user_card((get_mobile_payment_oper_id(user_id)[0]), callback_query.data[2:])

        if float(get_amount_from_user_mobile_payment_oper(user_id)[0]) >= (float(balance['msgrespdata']['response']['balance']) / 100):
            await bot.send_message(callback_query.from_user.id, get_dict('insufficient_funds', d))
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id, text=get_dict('section', d),
                                        reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
        else:
            access = InlineKeyboardMarkup().add(InlineKeyboardButton(get_dict('confirm', d), callback_data="0"))
            res = get_dict('confirm_transfer_card_to_card', d) + ' ' + callback_query.data[2:] + "\n" + get_dict('to_phone_number', d) + ': ' + get_to_phone_number_oper(user_id)[0] + '\n' + get_dict('amount', d) + ' ' + "{:,.2f}".format((int(get_amount_from_user_mobile_payment_oper(user_id)[0]))) +' '+get_dict('sum', d)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id, text=res, reply_markup=access)
    except Exception as e:
        logger_app.error("/handlers/money_transfer.py\nMethod: mp\n" + str(e))

@dp.callback_query_handler(lambda c: c.data == "0")
async def accessPayment(callback_query: types.CallbackQuery):
    try:

        user_id = callback_query.from_user.id
        d = get_lang(user_id)
        await bot.answer_callback_query(callback_query.id, )
        key = load_key()
        f = Fernet(key)
  
        encoded_card = get_card_encode(user_id, get_card_from_user_mobile_payment_oper(user_id))
        decrypted_card = f.decrypt(bytes((encoded_card[0])[2:-1], encoding='utf8'))

        errorCode = api.payCellular(decrypted_card.decode(), encoded_card[1], get_to_phone_number_oper(user_id)[0],
                                  str(get_amount_from_user_mobile_payment_oper(user_id)[0]))
     
        if errorCode["msgrespdata"]["errorCode"] == "0":
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, get_dict('sms_code', d), reply_markup=markups.cancel(d))
            set_user_state(user_id, get_state_by_key('S_SMS_TYPE_MOBILE_PAYMENT'))
            set_session_id(user_id, errorCode['msgrespdata']['response']['sessionId'])
            
        else:
            await bot.send_message(callback_query.from_user.id, get_dict('error_payment', d))
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, get_dict('section', d),
                                   reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
    except Exception as e:
        logger_app.error("/handlers/money_transfer.py\nMethod: accessPayment\n" + str(e))

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_SMS_TYPE_MOBILE_PAYMENT'))
async def sms(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
        else:
            sessionId = get_session_id(user_id)
            confirmCode = str(message.text)
            errorCode = (api.confirmOperationAuthCard(sessionId, confirmCode))['msgrespdata']['errorCode']
            
            if errorCode == '0':
                await bot.send_message(user_id, get_dict('success_transfer_card_to_card', d),
                                       reply_markup=markups.payments(d))
                set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
            else:
                await bot.send_message(user_id, get_dict('error_payment', d),
                                       reply_markup=markups.payments(d))
                set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: new_card_number\n" + str(e))
