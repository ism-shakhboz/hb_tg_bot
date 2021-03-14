from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_SETTINGS'))
async def settings(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('change_lang', d):
            if d == 1:
                await bot.send_message(user_id, get_dict('choose_lang', d), reply_markup=markups.change_lang_rus(d))
            elif d == 2:
                await bot.send_message(user_id, get_dict('choose_lang', d), reply_markup=markups.change_lang_latin(d))
            elif d == 3:
                await bot.send_message(user_id, get_dict('choose_lang', d), reply_markup=markups.change_lang_cyrillic(d))
            set_user_state(user_id, get_state_by_key('S_CHANGE_LANG'))
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/settings.py\nMethod: settings\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_CHANGE_LANG'))
async def change_lang(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if d == 1:
            if message.text == get_dict('lang_latin', d):
                set_lang(user_id, 2)
                d = get_lang(user_id)
                await bot.send_message(user_id, get_dict('lang_changed', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            elif message.text == get_dict('lang_cyrillic', d):
                set_lang(user_id, 3)
                d = get_lang(user_id)
                await bot.send_message(user_id, get_dict('lang_changed', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            elif message.text == get_dict('back', d):
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.settings(d))
                set_user_state(user_id, get_state_by_key('S_SETTINGS'))
            elif message.text == get_dict('main_menu', d):
                await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            else:
                await bot.send_message(user_id, get_dict('choose_lang', d))

        elif d == 2:
            if message.text == get_dict('lang_rus', d):
                set_lang(user_id, 1)
                d = get_lang(user_id)
                await bot.send_message(user_id, get_dict('lang_changed', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            elif message.text == get_dict('lang_cyrillic', d):
                set_lang(user_id, 3)
                d = get_lang(user_id)
                await bot.send_message(user_id, get_dict('lang_changed', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            elif message.text == get_dict('back', d):
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.settings(d))
                set_user_state(user_id, get_state_by_key('S_SETTINGS'))
            elif message.text == get_dict('main_menu', d):
                await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            else:
                await bot.send_message(user_id, get_dict('choose_lang', d))

        elif d == 3:
            if message.text == get_dict('lang_latin', d):
                set_lang(user_id, 2)
                d = get_lang(user_id)
                await bot.send_message(user_id, get_dict('lang_changed', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            elif message.text == get_dict('lang_rus', d):
                set_lang(user_id, 1)
                d = get_lang(user_id)
                await bot.send_message(user_id, get_dict('lang_changed', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            elif message.text == get_dict('back', d):
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.settings(d))
                set_user_state(user_id, get_state_by_key('S_SETTINGS'))
            elif message.text == get_dict('main_menu', d):
                await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
                set_user_state(user_id, get_state_by_key('S_GET_MAIN_MENU'))
            else:
                await bot.send_message(user_id, get_dict('choose_lang', d))
    except Exception as e:
        logger_app.error("/handlers/settings.py\nMethod: change_lang\n"+str(e))
