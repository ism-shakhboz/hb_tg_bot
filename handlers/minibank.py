from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


try:
    async def send_location(message, lang, user_id, code_branch):
        i = 0

        while i < len(code_branch_minibank(code_branch, lang)):
            if message == get_minibank_branch(code_branch, lang, code_branch_minibank(code_branch, lang)[i][0]):
                for j in get_minibank(code_branch, lang, code_branch_minibank(code_branch, lang)[i][0]):
                    await bot.send_location(user_id, j[3], j[4])
                    await bot.send_message(user_id, j[5])
                break
            i = i + 1

except Exception as e:
    logger_app.error("/handlers/atm.py\nMethod: send_location\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_MINI_BANK)
async def minibank(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        i = 0
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.branches(d))
            User().set_user_state(user_id, states.S_BRANCH)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            while i < len(distinct_regions()):
                if message.text == get_region(distinct_regions()[i][0], d):
                    await bot.send_message(user_id, get_dict('section', d),
                                           reply_markup=markups.minibank(distinct_regions()[i][0], d))
                    User().set_user_state(user_id, distinct_regions()[i][0] + 'M')
                    break
                i = i + 1
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '03M')
async def minibank_and(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)

        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '03')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_and\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '06M')
async def minibank_buk(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '06')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_buk\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '30M')
async def minibank_fer(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '30')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_fer\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '08M')
async def minibank_jiz(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '08')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_jiz\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '14M')
async def minibank_nam(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '14')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_nam\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '12M')
async def minibank_nav(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '12')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_nav\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '10M')
async def minibank_kash(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '10')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_kash\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '35M')
async def minibank_kar(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '35')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_kar\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '18M')
async def minibank_sam(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '18')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_sam\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '22M')
async def minibank_sur(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '22')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_sur\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '26M')
async def minibank_tashc(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '26')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_tashc\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '27M')
async def minibank_tashr(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '27')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_tashr\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '33M')
async def minibank_kho(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '33')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_kho\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '24M')
async def minibank_syr(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            User().set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '24')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: minibank_syr\n"+str(e))
