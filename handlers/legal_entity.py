from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import get_lang, set_user_state, get_user_state, get_dict, get_log, update_log, get_buttons


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_LEGAL_ENTITY)
async def legal_entity(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            set_user_state(user_id, states.S_GET_MAIN_MENU)
        elif message.text == get_dict('my_bills', d):
            await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.my_bills(d))
            set_user_state(user_id, states.S_BALANCE_OPER)
        elif message.text == get_dict('loans', d):
            if markups.buttons(d, 'legal_loans')["keyboard"][0][0] is None or markups.buttons(d, 'legal_loans')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_LEGAL_ENTITY)
                if get_buttons(d, 'legal_loans')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'legal_loans')[0][2], reply_markup=markups.inline_keyboards(d, 'legal_loans', get_buttons(d, 'legal_loans')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'legal_loans')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'legal_loans'))
                set_user_state(user_id, states.S_LOAN_LEGAL_ENTITY)
        elif message.text == get_dict('hamkor_pay_for_business', d):
            if markups.buttons(d, 'legal_accepting_payment')["keyboard"][0][0] is None or markups.buttons(d, 'legal_accepting_payment')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_LEGAL_ENTITY)
                if get_buttons(d, 'legal_accepting_payment')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'legal_accepting_payment')[0][2], reply_markup=markups.inline_keyboards(d, 'legal_accepting_payment', get_buttons(d, 'legal_accepting_payment')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'legal_accepting_payment')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'legal_accepting_payment'))
                set_user_state(user_id, states.S_LEGAL_ACCEPTING_PAYMENT)
        elif message.text == get_dict('deposit', d):
            if markups.buttons(d, 'legal_deposit')["keyboard"][0][0] is None or markups.buttons(d, 'legal_deposit')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_LEGAL_ENTITY)
                if get_buttons(d, 'legal_deposit')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'legal_deposit')[0][2], reply_markup=markups.inline_keyboards(d, 'legal_deposit', get_buttons(d, 'legal_deposit')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'legal_deposit')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'legal_deposit'))
                set_user_state(user_id, states.S_LEGAL_DEPOSIT)
        elif message.text == get_dict('other_services', d):
            if markups.buttons(d, 'legal_other_services')["keyboard"][0][0] is None or markups.buttons(d, 'legal_other_services')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_LEGAL_ENTITY)
                if get_buttons(d, 'legal_other_services')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'legal_other_services')[0][2], reply_markup=markups.inline_keyboards(d, 'legal_other_services', get_buttons(d, 'legal_other_services')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'legal_other_services')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'legal_other_services'))
                set_user_state(user_id, states.S_OTHER_SERVICES)
        elif message.text == get_dict('internet_banking', d):
            if markups.buttons(d, 'legal_internet_banking')["keyboard"][0][0] is None or markups.buttons(d, 'legal_internet_banking')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_LEGAL_ENTITY)
                if get_buttons(d, 'legal_internet_banking')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'legal_internet_banking')[0][2], reply_markup=markups.inline_keyboards(d, 'legal_internet_banking', get_buttons(d, 'legal_internet_banking')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'legal_internet_banking')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'legal_internet_banking'))
                set_user_state(user_id, states.S_LEGAL_ENTITY_INTERNET_BANKING)
        elif message.text == get_dict('tariffs', d):
            if markups.buttons(d, 'legal_entity_tariffs')["keyboard"][0][0] is None or markups.buttons(d, 'legal_entity_tariffs')["keyboard"][0][0]=='':
                set_user_state(user_id, states.S_LEGAL_ENTITY)
                if get_buttons(d, 'legal_entity_tariffs')[0][4]:
                    await bot.send_message(user_id, get_buttons(d, 'legal_entity_tariffs')[0][2], reply_markup=markups.inline_keyboards(d, 'legal_entity_tariffs', get_buttons(d, 'legal_entity_tariffs')[0][0]))
                else:
                    await bot.send_message(user_id, get_buttons(d, 'legal_entity_tariffs')[0][2])
            else:
                await bot.send_message(user_id, get_dict('section', d), reply_markup=markups.buttons(d, 'legal_entity_tariffs'))
                set_user_state(user_id, states.S_LEGAL_TARIFFS)
        else:
            await bot.send_message(user_id, get_dict('legal_entity_hint', d))
    except Exception as e:
        logger_app.error("/handlers/legal_entity.py\nMethod: legal_entity\n"+str(e))
