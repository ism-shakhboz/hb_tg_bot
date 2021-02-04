from aiogram import types
from misc import bot
from database_connection.dbcon import *

lang_m = types.ReplyKeyboardMarkup(resize_keyboard=True)
lang_m.row("🇷🇺 Русский", "🇺🇿 O'zbekcha", "🇺🇿 Ўзбекча")


async def get_markups(table_name, message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        j = 0
        for i in get_buttons(d, table_name):
            if message.text == i[1]:
                if i[4]:
                    await bot.send_message(user_id, i[2],
                                           reply_markup=inline_keyboards(d, table_name, i[0]))
                else:
                    await bot.send_message(user_id, i[2], reply_markup=reply_markup(d, i[3]))
                User().set_user_state(user_id, get_state(d, i[0], table_name))
            else:
                j = j + 1

        if j == len(get_buttons(d, table_name)):
            await bot.send_message(user_id, get_dict('section', d))
    except Exception as e:
        logger_app.error("\nMethod: " + table_name+'\n'+str(e))


def inline_keyboards(lang, table, name):
    keyboard = types.InlineKeyboardMarkup()
    for i in get_inline_markup(table, lang, name):
        for j in range(len(i[0].split(", "))):
            keyboard.add(types.InlineKeyboardButton(text=i[1].split(", ")[j], url=i[0].split(", ")[j]))
    return keyboard


def reply_markup(lang, state_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    c = []
    tup = []
    List = get_reply_markup(lang, state_id)
    for i in List:
        tup.append(i[0])

    if len(tup) % 2 != 0:
        for i in tup:
            if i != tup[-1]:
                c.append(i)
                count = count + 1
                if count == 2:
                    markup.row(c[0], c[1])
                    c.clear()
                    count = 0
            else:
                c.append(i)
                markup.row(c[0])
    else:
        for i in tup:
            c.append(i)
            count = count + 1
            if count == 2:
                markup.row(c[0], c[1])
                c.clear()
                count = 0
    return markup


def buttons(lang, table_name):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    c = []
    tup = []
    List = get_buttons(lang, table_name)
    for i in List:
        tup.append(i[1])

    if len(tup) % 2 != 0:
        for i in tup:
            if i != tup[-1]:
                c.append(i)
                count = count + 1
                if count == 2:
                    markup.row(c[0], c[1])
                    c.clear()
                    count = 0
            else:
                c.append(i)
                markup.row(c[0])
    else:
        for i in tup:
            c.append(i)
            count = count + 1
            if count == 2:
                markup.row(c[0], c[1])
                c.clear()
                count = 0
    return markup


def auth(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact = types.KeyboardButton(text=get_dict('send', d), request_contact=True)
    markup.add(contact)
    return markup


def cancel(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('cancel', d))
    return markup


def repayment_of_loans_bank_type(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('repayment_of_loans_bank_type_hamkorbank', d),
               get_dict('repayment_of_loans_bank_type_other', d))
    markup.row(get_dict('back', d))
    return markup


def payment_mobile_operators(user_id, d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_phone_number(user_id))
    markup.row(get_dict('cancel', d))
    return markup


def minibank(code, d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    c = []
    tup = []
    List = get_minibanks(code, d)
    for i in List:
        tup.append(i[3])

    if len(tup) % 2 != 0:
        for i in tup:
            if i != tup[-1]:
                c.append(i)
                count = count + 1
                if count == 2:
                    markup.row(c[0], c[1])
                    c.clear()
                    count = 0
            else:
                c.append(i)
                markup.row(c[0])
    else:
        for i in tup:
            c.append(i)
            count = count + 1
            if count == 2:
                markup.row(c[0], c[1])
                c.clear()
                count = 0
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def atm(code, d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    c = []
    tup = []
    List = get_atms(code, d)
    for i in List:
        tup.append(i[3])

    if len(tup) % 2 != 0:
        for i in tup:
            if i != tup[-1]:
                c.append(i)
                count = count + 1
                if count == 2:
                    markup.row(c[0], c[1])
                    c.clear()
                    count = 0
            else:
                c.append(i)
                markup.row(c[0])
    else:
        for i in tup:
            c.append(i)
            count = count + 1
            if count == 2:
                markup.row(c[0], c[1])
                c.clear()
                count = 0
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def districts(code, d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    c = []
    tup = []
    List = get_districts(code, d)
    for i in List:
        tup.append(i[3])

    if len(tup) % 2 != 0:
        for i in tup:
            if i != tup[-1]:
                c.append(i)
                count = count + 1
                if count == 2:
                    markup.row(c[0], c[1])
                    c.clear()
                    count = 0
            else:
                c.append(i)
                markup.row(c[0])
    else:
        for i in tup:
            c.append(i)
            count = count + 1
            if count == 2:
                markup.row(c[0], c[1])
                c.clear()
                count = 0
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def regions(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    c = []
    tup = []
    List = get_regions(d)
    for i in List:
        tup.append(i[0])

    if len(tup) % 2 != 0:
        for i in tup:
            if i != tup[-1]:
                c.append(i)
                count = count + 1
                if count == 2:
                    markup.row(c[0], c[1])
                    c.clear()
                    count = 0
            else:
                c.append(i)
                markup.row(c[0])
    else:
        for i in tup:
            c.append(i)
            count = count + 1
            if count == 2:
                markup.row(c[0], c[1])
                c.clear()
                count = 0
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def cost(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("100", "200")
    markup.row("300", "500")
    markup.row(get_dict('other_amount', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def calculator(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('purchase_currency', d), get_dict('sale_currency', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def branches(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('branches', d), get_dict('mini_bank', d))
    markup.row(get_dict('atm', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def exchange_rates(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('calculator', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def change_lang_cyrillic(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('lang_rus', d), get_dict('lang_latin', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def change_lang_latin(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('lang_rus', d), get_dict('lang_cyrillic', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def change_lang_rus(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('lang_latin', d), get_dict('lang_cyrillic', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def poll(d):
    keyboard = types.InlineKeyboardMarkup()
    url_btn1 = types.InlineKeyboardButton(text=get_dict('go_to_poll', d), url=(get_poll_url('poll_url', d))[0])
    keyboard.add(url_btn1)
    return keyboard


def loan_legal_entity_3_apply(d):
    keyboard = types.InlineKeyboardMarkup()
    url_btn1 = types.InlineKeyboardButton(text=get_dict('apply', d),
                                          url='http://hamkorbank.uz/application-legal-entities/')
    keyboard.add(url_btn1)
    return keyboard


def legal_entity_internet_banking(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('internet_banking', d), get_dict('mobile_banking', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def other_services(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('other_services_1', d), get_dict('other_services_2', d))
    markup.row(get_dict('other_services_3', d), get_dict('other_services_4', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def credit_legal(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('loan_legal_entity_1', d), get_dict('loan_legal_entity_2', d))
    markup.row(get_dict('loan_legal_entity_3', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def my_bills(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('balance_state', d))
    markup.row(get_dict('cardindex_1', d), get_dict('cardindex_2', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def zolotaya_korona(d):
    keyboard = types.InlineKeyboardMarkup()
    url_btn1 = types.InlineKeyboardButton(text=get_dict('download_hamkor_mobile_android', d),
                                          url=get_dict('url_hamkor_mobile_android', d))
    url_btn2 = types.InlineKeyboardButton(text=get_dict('download_hamkor_mobile_ios', d),
                                          url=get_dict('url_hamkor_mobile_ios', d))
    keyboard.add(url_btn1, url_btn2)
    return keyboard


def deposit_online_fc(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('contribution_online_7', d), get_dict('contribution_online_8', d))
    markup.row(get_dict('contribution_online_9', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def deposit_fc(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('contribution_foreign_currency_1', d), get_dict('contribution_foreign_currency_2', d))
    markup.row(get_dict('contribution_foreign_currency_3', d), get_dict('contribution_foreign_currency_4', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def contribution_national_currency_online(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('contribution_online_1', d), get_dict('contribution_online_2', d))
    markup.row(get_dict('contribution_online_3', d), get_dict('contribution_online_4', d))
    markup.row(get_dict('contribution_online_5', d), get_dict('contribution_online_6', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def contribution_national_currency_branches(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('contribution_national_currency_1', d), get_dict('contribution_national_currency_2', d))
    markup.row(get_dict('contribution_national_currency_3', d), get_dict('contribution_national_currency_4', d))
    markup.row(get_dict('contribution_national_currency_5', d), get_dict('contribution_national_currency_6', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def contribution_online_branch(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('online', d), get_dict('in_branches', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def visa_virtual(d):
    keyboard = types.InlineKeyboardMarkup()
    url_btn1 = types.InlineKeyboardButton(text=get_dict('download_hamkor_mobile_android', d),
                                          url=get_dict('url_hamkor_mobile_android', d))
    url_btn2 = types.InlineKeyboardButton(text=get_dict('download_hamkor_mobile_ios', d),
                                          url=get_dict('url_hamkor_mobile_ios', d))
    keyboard.add(url_btn1, url_btn2)
    return keyboard


def union_pay(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('union_pay_classic', d), get_dict('union_pay_exchange', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def visa(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('visa_gold', d), get_dict('visa_paywave_classic', d))
    markup.row(get_dict('visa_virtual', d), get_dict('visa_paywave_exchange', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def checkout(d):
    keyboard = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(text=get_dict('checkout', d), url=get_dict('url_card_online_application', d))
    keyboard.add(url_btn)
    return keyboard


def cards_menu(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('balance', d), get_dict('statement', d))
    markup.row(get_dict('block', d), get_dict('add_new_card', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def apply_loan(d):
    keyboard = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(text=get_dict('apply', d), url=get_dict('url_credit_registration', d))
    keyboard.add(url_btn)
    return keyboard


def mobile_application(d):
    keyboard = types.InlineKeyboardMarkup()
    url_btn1 = types.InlineKeyboardButton(text=get_dict('download_hamkor_mobile_android', d),
                                          url=get_dict('url_hamkor_mobile_android', d))
    url_btn2 = types.InlineKeyboardButton(text=get_dict('download_hamkor_mobile_ios', d),
                                          url=get_dict('url_hamkor_mobile_ios', d))
    keyboard.add(url_btn1, url_btn2)
    return keyboard


def money_transfers(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('soniya', d), get_dict('swift', d))
    markup.row(get_dict('corona', d), get_dict('unistream', d))
    markup.row(get_dict('contact', d), get_dict('moneygram', d))
    markup.row(get_dict('western_union', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def loans_individual(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('consumer_loan', d), get_dict('car_loan', d))
    markup.row(get_dict('mortgage', d), get_dict('micro_loan', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def deposits_individual(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('national_currency', d), get_dict('contribution_us_dollar', d))
    markup.row(get_dict('main_menu', d), get_dict('back', d))
    return markup


def cards(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('my_cards', d), get_dict('uzcard', d))
    markup.row(get_dict('humo', d), get_dict('visa', d))
    markup.row(get_dict('union_pay', d), get_dict('back', d))
    markup.row(get_dict('main_menu', d))
    return markup


def main_menu(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('payments', d), get_dict('individual', d))
    markup.row(get_dict('legal_entity', d), get_dict('contact_bank', d))
    markup.row(get_dict('news', d), get_dict('settings', d))
    markup.row(get_dict('general', d))
    return markup


def individual(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('mobile_application', d), get_dict('loans', d))
    markup.row(get_dict('cards', d), get_dict('contributions', d))
    markup.row(get_dict('money_transfers', d), get_dict('tariffs', d))
    markup.row(get_dict('back', d))
    return markup


def legal_entity(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('my_bills', d), get_dict('loans', d))
    markup.row(get_dict('hamkor_pay_for_business', d), get_dict('deposit', d))
    markup.row(get_dict('internet_banking', d), get_dict('other_services', d))
    markup.row(get_dict('tariffs', d), get_dict('back', d))
    return markup


def payments(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('card_to_card_transfers', d), get_dict('repayment_of_loans', d))
    markup.row(get_dict('mobile_operators', d))
    markup.row(get_dict('back', d))
    return markup


def general(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('exchange_rates', d), get_dict('branch_offices', d))
    markup.row(get_dict('back', d))
    return markup


def settings(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('change_lang', d))
    markup.row(get_dict('back', d))
    return markup


def feedback(d):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(get_dict('contact_centre', d), get_dict('online_consultant', d))
    markup.row(get_dict('social_network', d), get_dict('poll', d))
    markup.row(get_dict('back', d))
    return markup
