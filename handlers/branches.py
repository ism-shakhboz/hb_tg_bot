from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from os import path
from database_connection.dbcon import *

try:
    async def send_location(message, lang, user_id, code_region):
        i = 0
        while i < len(code_branch_b(code_region, lang)):
            if message == get_district(code_region, lang, code_branch_b(code_region, lang)[i][0]):

                for j in get_branches(code_region, lang, code_branch_b(code_region, lang)[i][0]):
                    await bot.send_photo(user_id, (get_image(j[1]+'.jpg'))[0])
                    await bot.send_location(user_id, j[3], j[4])
                    await bot.send_message(user_id, j[5])
                break
            i = i + 1
except Exception as e:
    logger_app.error("/handlers/branches.py\nMethod: send_location\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_BRANCH)
async def branch(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('branches', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('mini_bank', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_MINI_BANK)
        elif message.text == get_dict('atm', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('general_hint', d), reply_markup=markups.general(d))
            set_user_state(user_id, states.S_GENERAL)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: branch\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_BRANCH_OFFICE_REGION)
async def branch_office_region(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        i = 0
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.branches(d))
            set_user_state(user_id, states.S_BRANCH)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            while i < len(distinct_regions()):
                if message.text == get_region(distinct_regions()[i][0], d):
                    await bot.send_message(user_id, get_dict('section', d),
                                           reply_markup=markups.districts(distinct_regions()[i][0], d))
                    set_user_state(user_id, distinct_regions()[i][0] + 'B')
                    break
                i = i + 1
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: branch_office_region\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '03B')
async def bo_andijan(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '03')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_andijan\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '06B')
async def bo_bukhara(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '06')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_bukhara\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '30B')
async def bo_fergana(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '30')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_fergana\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '08B')
async def bo_jizzakh(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '08')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_jizzakh\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '14B')
async def bo_namangan(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '14')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_namangan\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '12B')
async def bo_navoi(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '12')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_navoi\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '10B')
async def bo_kashkadarya(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '10')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_kashkadarya\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '35B')
async def bo_karakalpak(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '35')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_karakalpak\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '18B')
async def bo_samarkand(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '18')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_samarkand\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '24B')
async def bo_sirdaryo(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '24')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_sirdaryo\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '22B')
async def bo_surkhandarya(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '22')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_surkhandarya\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '26B')
async def bo_tashkent(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '26')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_tashkent\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '27B')
async def bo_tashkent_reg(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '27')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_tashkent_reg\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '33B')
async def bo_khorezm(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_BRANCH_OFFICE_REGION)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            get_branches('33', d, '0041')
            await send_location(message.text, d, user_id, '33')
    except Exception as e:
        logger_app.error("/handlers/branches.py\nMethod: bo_khorezm\n" + str(e))
