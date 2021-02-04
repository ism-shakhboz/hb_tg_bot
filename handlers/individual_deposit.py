from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_CONTRIBUTION_INDIVIDUAL)
async def contribution(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('national_currency', d):
            await bot.send_message(user_id, get_dict('section', d),
                                   reply_markup=markups.contribution_online_branch(d))
            User().set_user_state(user_id, states.S_CONTRIBUTION_NATIONAL_CURRENCY)
        elif message.text == get_dict('contribution_us_dollar', d):
            await bot.send_message(user_id, get_dict('section', d),
                                   reply_markup=markups.contribution_online_branch(d))
            User().set_user_state(user_id, states.S_CONTRIBUTION_US_DOLLAR)
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('individual_hint', d), reply_markup=markups.individual(d))
            User().set_user_state(user_id, states.S_INDIVIDUAL)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/individual_deposit.py\nMethod: contribution\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_CONTRIBUTION_NATIONAL_CURRENCY)
async def contribution_national_currency(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('in_branches', d):
            if markups.buttons(d, 'individual_deposit_national_currency_branch')["keyboard"][0][0] is None or markups.buttons(d, 'individual_deposit_national_currency_branch')["keyboard"][0][0] == '':
                User().set_user_state(user_id, states.S_CONTRIBUTION_NATIONAL_CURRENCY)
                if get_buttons(d, 'individual_deposit_national_currency_branch')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_national_currency_branch')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_deposit_national_currency_branch', get_buttons(d,'individual_deposit_national_currency_branch')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_national_currency_branch')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_deposit_national_currency_branch'))
                User().set_user_state(user_id, states.S_CONTRIBUTION_NATIONAL_CURRENCY_BRANCHES)
        elif message.text == get_dict('online', d):
            if markups.buttons(d, 'individual_deposit_national_currency_online')["keyboard"][0][0] is None or markups.buttons(d, 'individual_deposit_national_currency_online')["keyboard"][0][0] == '':
                User().set_user_state(user_id, states.S_CONTRIBUTION_NATIONAL_CURRENCY)
                if get_buttons(d, 'individual_deposit_national_currency_online')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_national_currency_online')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_deposit_national_currency_online', get_buttons(d,'individual_deposit_national_currency_online')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_national_currency_online')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_deposit_national_currency_online'))
                User().set_user_state(user_id, states.S_CONTRIBUTION_NATIONAL_CURRENCY_ONLINE)
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.deposits_individual(d))
            User().set_user_state(user_id, states.S_CONTRIBUTION_INDIVIDUAL)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/individual_deposit.py\nMethod: contribution_national_currency\n"+str(e))


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_CONTRIBUTION_US_DOLLAR)
async def contribution_foreign_currency(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('in_branches', d):
            if markups.buttons(d, 'individual_deposit_foreign_currency_branch')["keyboard"][0][0] is None or markups.buttons(d, 'individual_deposit_foreign_currency_branch')["keyboard"][0][0] == '':
                User().set_user_state(user_id, states.S_CONTRIBUTION_US_DOLLAR)
                if get_buttons(d, 'individual_deposit_foreign_currency_branch')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_foreign_currency_branch')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_deposit_foreign_currency_branch', get_buttons(d,'individual_deposit_foreign_currency_branch')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_foreign_currency_branch')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_deposit_foreign_currency_branch'))
                User().set_user_state(user_id, states.S_CONTRIBUTION_FOREIGN_CURRENCY_BRANCHES)
        elif message.text == get_dict('online', d):
            if markups.buttons(d, 'individual_deposit_foreign_currency_online')["keyboard"][0][0] is None or markups.buttons(d, 'individual_deposit_foreign_currency_online')["keyboard"][0][0] == '':
                User().set_user_state(user_id, states.S_CONTRIBUTION_US_DOLLAR)
                if get_buttons(d, 'individual_deposit_foreign_currency_online')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_foreign_currency_online')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_deposit_foreign_currency_online', get_buttons(d,'individual_deposit_foreign_currency_online')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_deposit_foreign_currency_online')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_deposit_foreign_currency_online'))
                User().set_user_state(user_id, states.S_CONTRIBUTION_FOREIGN_CURRENCY_ONLINE)
        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.deposits_individual(d))
            User().set_user_state(user_id, states.S_CONTRIBUTION_INDIVIDUAL)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("/handlers/individual_deposit.py\nMethod: contribution_foreign_currency\n"+str(e))
