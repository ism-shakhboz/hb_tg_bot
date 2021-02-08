from misc import dp, bot, logger_p2p
from aiogram import types
import datetime as dt
from cryptography.fernet import Fernet
from vars import states, markups
from database_connection.dbcon import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import svgate

sessions = {}


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_CARD_TO_CARD'))
async def card_to_card_transfers(message: types.Message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('payments_hint', d), reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
        elif str(message.text).isdecimal() and len(str(message.text)) == 16:
            receiver = svgate.getCardName(message.text)        
            if receiver['msgrespdata']['errorCode'] == '0':
                await bot.send_message(user_id, get_dict('receiver', d) + receiver['msgrespdata']['response']['name'] + '\n' + get_dict('card_number', d) + message.text + '\n' + get_dict('enter_amount', d), reply_markup=markups.cancel(d))
                p2p_report_commit(user_id, first_name, last_name, message.text, str(dt.datetime.now()))
                set_p2p_oper_id_app_user(user_id, (get_p2p_oper_id(user_id)[0]))
                set_user_state(user_id, get_state_by_key('S_TYPE_SUM'))
            else:
                await bot.send_message(message.from_user.id, get_dict('recipient_not_found', d),
                                       reply_markup=markups.cancel(d))
        else:
            await bot.send_message(user_id, get_dict('error_enter_card_number', d), reply_markup=markups.cancel(d))
    except Exception as e:
        logger_p2p.error("/handlers/money_transfer.py\nMethod: card_to_card_transfers\n" + str(e))

def load_key():
    return open("secretCardDecodeKey.key", "rb").read()

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_TYPE_SUM'))
async def enter_amount(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if str(message.text).isnumeric():
            if float(message.text) < 1000:
                await bot.send_message(user_id, get_dict('minimum_sum_p2p', d))
                set_user_state(user_id, get_state_by_key('S_TYPE_SUM'))
            else:
                set_p2p_amount((get_p2p_oper_id(user_id)[0]), float(str(message.text)))
                set_p2p_info((get_p2p_oper_id(user_id)[0]), 'Enter amount', 'Summani kiriting', str(dt.datetime.now()))
                res = get_dict('choose_card', d)
                
                rows = get_all_cards(user_id)
                cards_inline = InlineKeyboardMarkup()
                if len(rows) > 0:
                    for row in rows:
                        cards_inline.add(InlineKeyboardButton(row[0] + ' '+row[1], callback_data = "p2p"+row[0]))
                        
                    await bot.send_message(user_id, res, reply_markup=cards_inline)
                else:
                    await bot.send_message(user_id, get_dict('card_check', d))
        elif message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
        else:
            await bot.send_message(user_id, get_dict('error_enter_amount_p2p', d), reply_markup=markups.cancel(d))
    except Exception as e:
        logger_p2p.error("/handlers/money_transfer.py\nMethod: enter_amount\n" + str(e))


@dp.callback_query_handler(lambda c: c.data.find("p2p") > -1)
async def p2p(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        d = get_lang(user_id)
        key = load_key()
        f = Fernet(key)
        
        encoded_card = get_card_encode(user_id, callback_query.data[3:])
        decrypted_card = f.decrypt(bytes((encoded_card[0])[2:-1], encoding='utf8'))
        balance = svgate.getCardBalance(decrypted_card.decode(), encoded_card[1])
       
        set_p2p_from_user_card((get_p2p_oper_id(user_id)[0]), callback_query.data[3:])

        
        if float(get_amount_from_user_p2p_oper(user_id)[0]) >= (float(balance['msgrespdata']['response']['balance'])/100):
            set_p2p_info((get_p2p_oper_id(user_id)[0]), 'Error: Unsufficient funds', 'Mablag'' yetarli emas', str(dt.datetime.now()))
            await bot.send_message(callback_query.from_user.id, get_dict('insufficient_funds', d))
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id, text=get_dict('section', d),
                                        reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
        else:
            access = InlineKeyboardMarkup().add(InlineKeyboardButton(get_dict('confirm', d), callback_data="access"+callback_query.data[3:]))
            res = get_dict('confirm_transfer_card_to_card', d) + ' ' +callback_query.data[3:] + "\n" + get_dict('to_card', d)+' '+get_to_card_p2p_oper(user_id)[0]+'\n'+get_dict('amount', d)+' '+ "{:,.2f}".format((int(get_amount_from_user_p2p_oper(user_id)[0])))+' '+get_dict('sum', d)

            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id, text=res, reply_markup=access)
    except Exception as e:
        logger_p2p.error("/handlers/money_transfer.py\nMethod: p2p\n" + str(e))


@dp.callback_query_handler(lambda c: c.data.find("access") > -1)
async def access(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        d = get_lang(user_id)
        await bot.answer_callback_query(callback_query.id, )
        key = load_key()
        f = Fernet(key)
        
        encoded_card = get_card_encode(user_id, callback_query.data[6:])
        decrypted_card = f.decrypt(bytes((encoded_card[0])[2:-1], encoding='utf8'))
        
        errorCode = svgate.payP2p(decrypted_card.decode(), encoded_card[1], get_to_card_p2p_oper(user_id)[0], str(get_amount_from_user_p2p_oper(user_id)[0]))
       
        if errorCode["msgrespdata"]["errorCode"] == "0":
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, get_dict('sms_code', d), reply_markup=markups.cancel(d))
            set_p2p_info((get_p2p_oper_id(user_id)[0]), 'SMS', 'SMS kodni kiriting', str(dt.datetime.now()))
           
            set_session_id(user_id, errorCode['msgrespdata']['response']['sessionId'])
            set_user_state(user_id, get_state_by_key('S_SMS_TYPE_P2P'))
        else:
            await bot.send_message(callback_query.from_user.id,
                                   get_dict('error_transfer_card_to_card', d) + errorCode["msgrespdata"]["errorMessage"])

            set_p2p_info((get_p2p_oper_id(user_id)[0]), errorCode["msgrespdata"]["errorMessage"], 'Xatolik yuzaga keldi',
                         str(dt.datetime.now()))
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, get_dict('section', d),
                                   reply_markup=markups.payments(d))
            set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
    except Exception as e:
        logger_p2p.error("/handlers/money_transfer.py\nMethod: access\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_SMS_TYPE_P2P'))
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
            errorCode = (svgate.confirmOperationAuthCard(sessionId, confirmCode))['msgrespdata']['errorCode']
            if errorCode == '0':
                await bot.send_message(user_id, get_dict('success_transfer_card_to_card', d), reply_markup=markups.payments(d))
                set_p2p_info((get_p2p_oper_id(user_id)[0]), 'Success', 'To''lov amalga oshirildi', str(dt.datetime.now()))
                set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
            else:
                await bot.send_message(user_id, get_dict('error_transfer_card_to_card', d), reply_markup=markups.payments(d))
                set_user_state(user_id, get_state_by_key('S_PAYMENTS'))
    except Exception as e:
        logger_p2p.error("/handlers/individual_cards.py\nMethod: new_card_number\n" + str(e))
