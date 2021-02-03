from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *
from parsing_data.exchange_rate_parsing import purchase_calculator, sale_calculator
from parsing_data import exchange_rate_parsing


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_EXCHANGE_RATES)
async def exchange_rates(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('calculator', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.calculator(d))
            set_user_state(user_id, states.S_CALCULATOR)
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('general_hint', d), reply_markup=markups.general(d))
            set_user_state(user_id, states.S_GENERAL)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await bot.send_message(user_id, get_dict('exchange_rates_data', d), reply_markup=markups.exchange_rates(d))
    except Exception as e:
        logger_app.error("/handlers/exchange_rates.py\nMethod: exchange_rates\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_CALCULATOR)
async def calculator(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('purchase_currency', d):
            await bot.send_message(user_id, get_dict('purchase_warning', d), reply_markup=markups.cost(d))
            set_user_state(user_id, states.S_PURCHASE_CURRENCY)
        elif message.text == get_dict('sale_currency', d):
            await bot.send_message(user_id, get_dict('sale_warning', d), reply_markup=markups.cost(d))
            set_user_state(user_id, states.S_SALE_CURRENCY)
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('cb_currency_rate', d)+' \n\n '+exchange_rate_parsing.cb_ex_rates+'\n\n\n'+get_dict('purchase_sale', d)+'\n\n'+exchange_rate_parsing.purchase_sale_ex_rates, reply_markup=markups.exchange_rates(d))
            set_user_state(user_id, states.S_EXCHANGE_RATES)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/exchange_rates.py\nMethod: calculator\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_PURCHASE_CURRENCY)
async def purchase_currency(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.calculator(d))
            set_user_state(user_id, states.S_CALCULATOR)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        elif message.text == get_dict('other_amount', d):
            await bot.send_message(user_id, get_dict('enter_amount', d))
        else:
            try:
                result = purchase_calculator(int(message.text), d)
                await bot.send_message(user_id, result)
                return
            except ValueError:
                try:
                    result = purchase_calculator(float(message.text), d)
                    await bot.send_message(user_id, result)
                    return
                except ValueError:
                    await bot.send_message(user_id, get_dict('error_enter_number', d))
    except Exception as e:
        logger_app.error("/handlers/exchange_rates.py\nMethod: purchase_currency\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_SALE_CURRENCY)
async def sale_currency(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.calculator(d))
            set_user_state(user_id, states.S_CALCULATOR)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        elif message.text == get_dict('other_amount', d):
            await bot.send_message(user_id, get_dict('enter_amount', d))
        else:
            try:
                result = sale_calculator(int(message.text), d)
                await bot.send_message(user_id, result)
                return
            except ValueError:
                try:
                    result = sale_calculator(float(message.text), d)
                    await bot.send_message(user_id, result)
                    return
                except ValueError:
                    await bot.send_message(user_id, get_dict('error_enter_number', d))
    except Exception as e:
        logger_app.error("/handlers/exchange_rates.py\nMethod: sale_currency\n"+str(e))
