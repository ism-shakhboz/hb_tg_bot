from psycopg2._psycopg import Error
from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
import datetime as dt
import svgate
from aiogram.types import ReplyKeyboardRemove
from random import randint
import json
from database_connection.dbcon import *


@dp.message_handler(content_types=['photo'])
async def image(message: types.Message):
    file_info = await bot.get_file(message.photo[-1].file_id)
    image_insert(file_info['file_id'], message.caption+'.jpg')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        user = get_user(user_id)

        if user is None:
            await bot.send_message(user_id, "Выберите язык / Tilni tanlang / Тилни танланг", reply_markup=markups.lang_m)
            add_user(user_id, '', first_name, last_name, username, states.S_START)
        else:
            status = get_user_status(user_id)
            if get_user_status(user_id)=='0':
              
                await bot.send_message(user_id, "Выберите язык / Tilni tanlang / Тилни танланг", reply_markup=markups.lang_m)
                set_user_state(user_id, states.S_START)
            else:
                d = get_lang(user_id)
             
                await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, states.S_GET_MAIN_MENU)
    except Exception as e:
        logger_app.error("/handlers/bot.py\nMethod: start\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_START)
async def lang(message: types.Message):
    try:
        user_id = message.from_user.id
        if message.text == "🇺🇿 O'zbekcha":
            set_lang(user_id, 'uz')
            await bot.send_message(user_id, get_dict('send_phone_number', 'uz'), reply_markup=markups.auth('uz'))
        elif message.text == "🇷🇺 Русский":
            set_lang(user_id, 'ru')
            await bot.send_message(user_id, get_dict('send_phone_number', 'ru'), reply_markup=markups.auth('ru'))
        elif message.text == "🇺🇿 Ўзбекча":
            set_lang(user_id, 'cy')
            await bot.send_message(user_id, get_dict('send_phone_number', 'cy'), reply_markup=markups.auth('cy'))
        else:
            await bot.send_message(message.from_user.id, "Tilni tanlang/Выберите язык", reply_markup=markups.lang_m)
            set_user_state(user_id, states.S_START)
    except Exception as e:
        logger_app.error("/handlers/bot.py\nMethod: lang\n" + str(e))


# str(message.contact.phone_number).replace('+', '')
@dp.message_handler(content_types=['contact'])
async def auth(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        set_phone_number(user_id, str(message.contact.phone_number).replace('+', ''))
        set_timer_sms(user_id, str(dt.datetime.now() + dt.timedelta(minutes=1)))
        otp = randint(100000, 999999)
        set_code(user_id, otp)
        script = 'SELECT "ID" FROM playmobile_report order by "ID" DESC LIMIT 1'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        svgate.get_sms(message.contact.phone_number, otp, (int(cur.fetchone()[0])+1))
        playmobile_insert(user_id, 'Message is: ' + str(otp), str(dt.datetime.now()))
        await bot.send_message(user_id, get_dict('sms_code', d), reply_markup = ReplyKeyboardRemove())
        set_user_state(user_id, states.S_CONFIRM_NUMBER)
    except Exception as e:
        logger_app.error("/handlers/bot.py\nMethod: auth\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_CONFIRM_NUMBER)
async def confirm_number(message: types.Message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        d = get_lang(user_id)
        get_expire = 'SELECT expire FROM app_users where user_id=(%s);'
        cur = conn.cursor()
        cur.execute(get_expire, (str(user_id),))
        row = cur.fetchone()
        if row[0] > dt.datetime.now():
            if message.text == str(get_code(user_id)):
                set_log(user_id, get_phone_number(user_id))
                update_user_status(user_id)
                await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, states.S_GET_MAIN_MENU)
            else:
                await bot.send_message(user_id, get_dict('error_sms_code', d))
        else:
         
            await bot.send_message(user_id, "Выберите язык / Tilni tanlang / Тилни танланг", reply_markup=markups.lang_m)
            set_user_state(user_id, states.S_START)
           
    except Exception as e:
        logger_app.error("/handlers/bot.py\nMethod: confirm_number\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_GET_MAIN_MENU)
async def main_menu(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('individual', d):
            await bot.send_message(user_id, get_dict('individual_hint', d), reply_markup=markups.individual(d))
            set_user_state(user_id, states.S_INDIVIDUAL)
        elif message.text == get_dict('legal_entity', d):
            await bot.send_message(user_id, get_dict('legal_entity_hint', d), reply_markup=markups.legal_entity(d))
            set_user_state(user_id, states.S_LEGAL_ENTITY)
        elif message.text == get_dict('payments', d):
            await bot.send_message(user_id, get_dict('payments_hint', d), reply_markup=markups.payments(d))
            set_user_state(user_id, states.S_PAYMENTS)
        elif message.text == get_dict('news', d):
            await bot.send_message(user_id, get_news(d))
        elif message.text == get_dict('general', d):
            await bot.send_message(user_id, get_dict('general_hint', d), reply_markup=markups.general(d))
            set_user_state(user_id, states.S_GENERAL)
        elif message.text == get_dict('settings', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.settings(d))
            set_user_state(user_id, states.S_SETTINGS)
        elif message.text == get_dict('contact_bank', d):
            if markups.buttons(d, 'feedback')["keyboard"][0][0] is None or markups.buttons(d, 'feedback')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_GET_MAIN_MENU)
                if get_buttons(d, 'feedback')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'feedback')[0][2], reply_markup=markups.inline_keyboards(d, 'feedback', get_buttons(d, 'feedback')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'feedback')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'feedback'))
                set_user_state(user_id, states.S_FEEDBACK)
        else:
            await bot.send_message(user_id, get_dict('main_menu_hint', d))
    except Exception as e:
        logger_app.error("/handlers/bot.py\nMethod: main_menu\n" + str(e))
