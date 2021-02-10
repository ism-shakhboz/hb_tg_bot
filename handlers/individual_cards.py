from misc import dp, bot
from aiogram import types
from vars import states, markups
from cryptography.fernet import Fernet
from database_connection.dbcon import *
import json
import api


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_CARD'))
async def cards(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        cards = ''
        if message.text == get_dict('my_cards', d):
            cardsList = get_card_json(user_id)
            if len(cardsList) > 0:
                for card in cardsList:
                    cards = cards + card[1] + '\n'
                await bot.send_message(user_id, get_dict('your_cards', d)+'\n\n'+cards, reply_markup=markups.cards_menu(d))
                cards=''
            else:
                await bot.send_message(user_id, get_dict('card_check', d), reply_markup=markups.cards_menu(d))
            set_user_state(user_id, get_state_by_key('S_CARD_MENU'))
        elif message.text == get_dict('uzcard', d):
            if markups.buttons(d, 'individual_cards_uzcard')["keyboard"][0][0] is None or markups.buttons(d, 'individual_cards_uzcard')["keyboard"][0][0] == '':
                set_user_state(user_id, get_state_by_key('S_CARD'))
                if get_buttons(d, 'individual_cards_uzcard')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_uzcard')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_cards_uzcard', get_buttons(d,'individual_cards_uzcard')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_uzcard')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_cards_uzcard'))
                set_user_state(user_id, get_state_by_key('S_UZCARD'))
        elif message.text == get_dict('humo', d):
            if markups.buttons(d, 'individual_cards_humo')["keyboard"][0][0] is None or markups.buttons(d, 'individual_cards_humo')["keyboard"][0][0] == '':
                set_user_state(user_id, get_state_by_key('S_CARD'))
                if get_buttons(d, 'individual_cards_humo')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_humo')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_cards_humo', get_buttons(d,'individual_cards_humo')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_humo')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_cards_humo'))
                set_user_state(user_id, get_state_by_key('S_HUMO'))
        elif message.text == get_dict('visa', d):
            if markups.buttons(d, 'individual_cards_visa')["keyboard"][0][0] is None or markups.buttons(d, 'individual_cards_visa')["keyboard"][0][0] == '':
                set_user_state(user_id, get_state_by_key('S_CARD'))
                if get_buttons(d, 'individual_cards_visa')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_visa')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_cards_visa', get_buttons(d,'individual_cards_visa')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_visa')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_cards_visa'))
                set_user_state(user_id, get_state_by_key('S_VISA'))
        elif message.text == get_dict('union_pay', d):
            if markups.buttons(d, 'individual_cards_unionpay')["keyboard"][0][0] is None or markups.buttons(d, 'individual_cards_unionpay')["keyboard"][0][0] == '':
                set_user_state(user_id, get_state_by_key('S_CARD'))
                if get_buttons(d, 'individual_cards_unionpay')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_unionpay')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_cards_unionpay', get_buttons(d,'individual_cards_unionpay')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_cards_unionpay')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_cards_unionpay'))
                set_user_state(user_id, get_state_by_key('S_UNION_PAY'))
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('individual_hint', d), reply_markup=markups.individual(d))
            set_user_state(user_id, get_state_by_key('S_INDIVIDUAL'))
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: cards\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_CARD_MENU'))
async def card_menu(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('balance', d):
            cards_list = get_all_cards(user_id)
            res = ''
            if len(cards_list)>0:
                key = load_key()
                f = Fernet(key)
                res = get_dict('card_balance', d) + '\n\n'
                for row in cards_list:
                    decrypted_card = f.decrypt(bytes((row[2])[2:-1], encoding='utf8'))
                    balance = api.getCardBalance(decrypted_card.decode(), row[1])
                    if balance['msgrespdata']['errorCode'] == '0':
                        res = res + "💳 " + row[0] + '\n💰' + "{:,.2f}".format((int(balance["msgrespdata"]["response"]["balance"])/100)) + ' ' +get_dict('sum', d)+'\n\n'
                await bot.send_message(user_id, res)
            else:
                await bot.send_message(user_id, get_dict('card_check', d))
        elif message.text == get_dict('statement', d):
            await bot.send_message(user_id, get_dict('developing', d))
        elif message.text == get_dict('block', d):
            await bot.send_message(user_id, get_dict('developing', d))
        elif message.text == get_dict('refresh_card', d):
            refresh_cards = api.get_cards(get_phone_number(user_id))['result']
            cards = ''
            if refresh_cards:
                update(user_id, refresh_cards)
                card_json = get_card_json(user_id)
                if len(card_json)>0: 
                    for row in card_json:
                        status = ""
                        card = json.loads(row[1])
                        
                        if card["result"]["status"] == 0:
                            status = "✅"
                        else:
                            status = "❌"
                        cards = cards+''+status+' '+card["result"]["pan"]+'\n'
                await bot.send_message(user_id, get_dict('refresh_card_success', d)+'\n\n'+cards)
            else:
                await bot.send_message(user_id, get_dict('card_check', d))
        elif message.text == get_dict('add_new_card', d):
            await bot.send_message(user_id, get_dict('add_new_card_number', d), reply_markup=markups.cancel(d))
            set_user_state(user_id, get_state_by_key('S_NEW_CARD_NUMBER'))
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.cards(d))
            set_user_state(user_id, get_state_by_key('S_CARD'))
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: card_menu\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_NEW_CARD_NUMBER'))
async def new_card_number(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            script = 'UPDATE app_users SET new_card_number=(%s) WHERE user_id=(%s);'
            cur = conn.cursor()
            cur.execute(script, ('', user_id))
            conn.commit()
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.cards_menu(d))
            set_user_state(user_id, get_state_by_key('S_CARD_MENU'))
        elif str(message.text).isdecimal() and len(str(message.text)) == 16:
            script = 'UPDATE app_users SET new_card_number=(%s) WHERE user_id=(%s);'
            cur = conn.cursor()
            cur.execute(script, (str(message.text), user_id))
            conn.commit()
            await bot.send_message(user_id, get_dict('add_new_card_expiry', d), reply_markup=markups.cancel(d))
            set_user_state(user_id, get_state_by_key('S_NEW_CARD_EXPIRY'))
        else:
            await bot.send_message(user_id, get_dict('error_enter_card_number', d), reply_markup=markups.cancel(d))
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: new_card_number\n" + str(e))

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_NEW_CARD_EXPIRY'))
async def new_card_expiry(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            script = 'UPDATE app_users SET new_card_number=(%s), new_card_expiry=(%s) WHERE user_id=(%s);'
            cur = conn.cursor()
            cur.execute(script, ('', '', user_id))
            conn.commit()
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.cards_menu(d))
            set_user_state(user_id, get_state_by_key('S_CARD_MENU'))
        elif str(message.text).isdecimal() and len(str(message.text)) == 4:
            script = 'UPDATE app_users SET new_card_expiry=(%s) WHERE user_id=(%s);'
            cur = conn.cursor()
            cur.execute(script, (str(message.text), user_id))
            conn.commit()

            script = 'SELECT new_card_number, new_card_expiry FROM app_users WHERE user_id=(%s);'
            cur = conn.cursor()
            cur.execute(script, (str(user_id),))
            row = cur.fetchone()
            respJson = api.authCard(row[0], row[1])
            errorCode = respJson['msgrespdata']['errorCode']
            if errorCode == '0':
                await bot.send_message(user_id, get_dict('sms_code', d), reply_markup=markups.cancel(d))
                set_session_id(user_id, respJson['msgrespdata']['response']['sessionId'])
                set_user_state(user_id, get_state_by_key('S_SMS_TYPE_AUTH_CARD'))
            else:
                await bot.send_message(user_id, get_dict('error_add_card', d), reply_markup=markups.cards_menu(d))
                set_user_state(user_id, get_state_by_key('S_CARD_MENU'))
        else:
            await bot.send_message(user_id, get_dict('error_enter_card_expiry', d), reply_markup=markups.cancel(d))
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: new_card_number\n" + str(e))

def load_key():
    return open("secretCardDecodeKey.key", "rb").read()


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_SMS_TYPE_AUTH_CARD'))
async def sms(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cancel', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.cards_menu(d))
            set_user_state(user_id, get_state_by_key('S_CARD_MENU'))
        else:
            sessionId = get_session_id(user_id)
            confirmCode = str(message.text)
            errorCode = (api.confirmOperationAuthCard(sessionId, confirmCode))['msgrespdata']['errorCode']
            
            if errorCode == '0':
                cards=''
                key = load_key()
                encoded_card_number = (get_card(user_id)[0]).encode()
                f = Fernet(key)
                encrypted_card_number = f.encrypt(encoded_card_number)
                card_mask = (get_card(user_id)[0])[:6] + '*' * 6 + (get_card(user_id)[0])[-4:]
                authCard(user_id, card_mask, get_card(user_id)[1], str(encrypted_card_number))
                
                await bot.send_message(user_id, get_dict('added_new_card', d)+'\n', reply_markup=markups.cards_menu(d))
                cardsList = get_card_json(user_id)
                for card in cardsList:
                    cards = cards + card[1] + '\n'
                await bot.send_message(user_id, get_dict('your_cards', d)+'\n\n'+cards, reply_markup=markups.cards_menu(d))
                cards=''
                set_user_state(user_id, get_state_by_key('S_CARD_MENU'))
            else:
                await bot.send_message(user_id, get_dict('error_add_card', d), reply_markup=markups.cards_menu(d))
                set_user_state(user_id, get_state_by_key('S_CARD_MENU'))
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: new_card_number\n" + str(e))
        
     

@dp.callback_query_handler(lambda c: c.data.find("block") == 0)
async def process_callback_block(callback_query: types.CallbackQuery):
    try:
        d = get_lang(callback_query.from_user.id)
        await bot.answer_callback_query(callback_query.id)
        res = get_dict('card', d)+" "
        block = api.card_status_change(callback_query.data.replace("block", ""), 20)['result']
       
        if block:
            if block["status"] == "OK":
                res += block["pan"] + " " +get_dict('blocked', d)
            else:
                res += block["pan"] + " "+ get_dict('error_block', d)
        refresh_cards = api.get_cards(get_phone_number(callback_query.from_user.id))['result']
        if refresh_cards:
            update(callback_query.from_user.id, refresh_cards)
        await bot.send_message(callback_query.from_user.id, res)
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: process_callback_block\n" + str(e))
        

@dp.callback_query_handler(lambda c: c.data.find("history") > -1)
async def process_callback_history(callback_query: types.CallbackQuery):
    try:
        d = get_lang(callback_query.from_user.id)
        await bot.answer_callback_query(callback_query.id)
        res = get_dict('card_history', d)+'\n'
        
        contents = api.get_history(ids=[callback_query.data.replace("history", "")])["result"]["content"]
        
        if len(contents) > 0:
            for content in contents:
                if content["isCredit"]:
                    res += str(content["udate"])[6:] + '.' + str(content["udate"])[4:6] + '.' + str(content["udate"])[:4] + ' ' + str(content["utime"])[0:2] + ':' + str(content["utime"])[2:4] + ':' + str(content["utime"])[4:6] + "  " + '+' + "{:.2f}".format(
                        (content["actamt"] / 100)) + "\n"
                else:
                    res += str(content["udate"])[6:]+'.' +str(content["udate"])[4:6]+'.'+str(content["udate"])[:4]+' '+str(content["utime"])[0:2]+':'+str(content["utime"])[2:4]+':'+str(content["utime"])[4:6]+"  "+'-'+ "{:.2f}".format((content["actamt"] / 100))+"\n"
            await bot.send_message(callback_query.from_user.id, res, reply_markup=markups.cards_menu(d))
        else:
            await bot.send_message(callback_query.from_user.id, get_dict('no_data_statement', d), reply_markup=markups.cards_menu(d))
    except Exception as e:
        logger_app.error("/handlers/individual_cards.py\nMethod: process_callback_history\n" + str(e))
