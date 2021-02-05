from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_INDIVIDUAL)
async def individual(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('cards', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.cards(d))
            set_user_state(user_id, states.S_CARD)
        elif message.text == get_dict('contributions', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.deposits_individual(d))
            set_user_state(user_id, states.S_CONTRIBUTION_INDIVIDUAL)
        elif message.text == get_dict('loans', d):
            if markups.buttons(d, 'individual_loans')["keyboard"][0][0] is None or markups.buttons(d, 'individual_loans')["keyboard"][0][0] == '':
                set_user_state(user_id, states.S_INDIVIDUAL)
                if get_buttons(d, 'individual_loans')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_loans')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_loans', get_buttons(d,'individual_loans')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_loans')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_loans'))
                set_user_state(user_id, states.S_LOAN)
        elif message.text == get_dict('money_transfers', d):
            if markups.buttons(d, 'individual_money_transfer')["keyboard"][0][0] is None or markups.buttons(d, 'individual_money_transfer')["keyboard"][0][0] == '':
                set_user_state(user_id, states.S_INDIVIDUAL)
                if get_buttons(d, 'individual_money_transfer')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_money_transfer')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_money_transfer', get_buttons(d,'individual_money_transfer')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_money_transfer')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_money_transfer'))
                set_user_state(user_id, states.S_MONEY_TRANSFER)
        elif message.text == get_dict('tariffs', d):
            if markups.buttons(d, 'individual_tariffs')["keyboard"][0][0] is None or markups.buttons(d, 'individual_tariffs')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_INDIVIDUAL)
                if get_buttons(d, 'individual_tariffs')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_tariffs')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_tariffs', get_buttons(d, 'individual_tariffs')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_tariffs')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_tariffs'))
                set_user_state(user_id, states.S_INDIVIDUAL_TARIFFS)
        elif message.text == get_dict('mobile_application', d):
            if markups.buttons(d, 'individual_mobile_app')["keyboard"][0][0] is None or markups.buttons(d, 'individual_mobile_app')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_INDIVIDUAL)
                if get_buttons(d, 'individual_mobile_app')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'individual_mobile_app')[0][2], reply_markup=markups.inline_keyboards(d, 'individual_mobile_app', get_buttons(d, 'individual_mobile_app')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'individual_mobile_app')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'individual_mobile_app'))
                set_user_state(user_id, states.S_INDIVIDUAL_MOBILE)

        elif message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        else:
            await bot.send_message(user_id, get_dict('individual_hint', d))
    except Exception as e:
        logger_app.error("/handlers/individual.py\nMethod: individual\n" + str(e))
