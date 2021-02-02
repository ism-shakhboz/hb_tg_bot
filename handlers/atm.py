from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import get_lang, set_user_state, get_user_state, get_dict, get_log, update_log, get_region, \
    get_atm_branch, get_atm, distinct_regions, code_branch_atm


try:
    async def send_location(message, lang, user_id, code_branch):
        i = 0
        while i < len(code_branch_atm(code_branch, lang)):
            if message == get_atm_branch(code_branch, lang, code_branch_atm(code_branch, lang)[i][0]):
                for j in get_atm(code_branch, lang, code_branch_atm(code_branch, lang)[i][0]):
                    await bot.send_location(user_id, j[3], j[4])
                    await bot.send_message(user_id, j[5])
                break
            i = i + 1
except Exception as e:
    logger_app.error("/handlers/atm.py\nMethod: send_location\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_ATM)
async def atm(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)

        i = 0
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.branches(d))
            set_user_state(user_id, states.S_BRANCH)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            while i < len(distinct_regions()):
                if message.text == get_region(distinct_regions()[i][0], d):
                    await bot.send_message(user_id, get_dict('section', d),
                                           reply_markup=markups.atm(distinct_regions()[i][0], d))
                    set_user_state(user_id, distinct_regions()[i][0] + 'A')
                    break
                i = i + 1
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm\n" + str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '03A')
async def atm_and(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)

        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '03')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_and\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '06A')
async def atm_buk(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '06')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_buk\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '30A')
async def atm_fer(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '30')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_fer\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '14A')
async def atm_nam(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '14')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_nam\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '26A')
async def atm_tashc(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '26')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_tashc\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '27A')
async def atm_tashr(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '27')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_tashr\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '18A')
async def atm_sam(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '18')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_sam\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '12A')
async def atm_nav(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '12')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_nav\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '22A')
async def atm_sur(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '22')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_sur\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '08A')
async def atm_jiz(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '08')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_jiz\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '33A')
async def atm_kho(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '33')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_kho\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '35A')
async def atm_kar(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '35')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_kar\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '10A')
async def atm_kash(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '10')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_kash\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == '24A')
async def atm_syr(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.regions(d))
            set_user_state(user_id, states.S_ATM)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await send_location(message.text, d, user_id, '24')
    except Exception as e:
        logger_app.error("/handlers/atm.py\nMethod: atm_syr\n"+str(e))
