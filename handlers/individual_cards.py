from misc import dp, bot
from aiogram import types
from vars import markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_CARD'))
async def cards(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('uzcard', d):
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