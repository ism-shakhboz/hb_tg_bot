from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *
from parsing_data import exchange_rate_parsing


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_GENERAL)
async def general(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('exchange_rates', d):
            await bot.send_message(user_id, get_dict('cb_currency_rate', d)+' \n\n '+exchange_rate_parsing.cb_ex_rates+'\n\n\n'+get_dict('purchase_sale', d)+'\n\n'+exchange_rate_parsing.purchase_sale_ex_rates, reply_markup=markups.exchange_rates(d))
            User().set_user_state(user_id, states.S_EXCHANGE_RATES)
        elif message.text == get_dict('branch_offices', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.branches(d))
            User().set_user_state(user_id, states.S_BRANCH)
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
    except Exception as e:
        logger_app.error("/handlers/general.py\nMethod: general\n"+str(e))