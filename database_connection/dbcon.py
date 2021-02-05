import psycopg2
from psycopg2 import Error, sql
import svgate
import json
import configparser
import urllib3
import datetime as dt
from misc import logger_app

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = configparser.ConfigParser()
config.read("config.ini")

conn = psycopg2.connect(
    database=config['DATABASE']['DBName'],
    user=config['DATABASE']['user'],
    password=config['DATABASE']['password'],
    host=config['DATABASE']['host'],
    port=config['DATABASE']['port']
)

def get_card_encode(user_id, card_number):
    try:
        script = 'SELECT encrypted_card_number, card_expiry FROM cards WHERE user_id=(%s) AND card_number=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id), card_number))
        cards = cur.fetchone()
        return cards
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_card_encode\n" + str(e))

def get_all_cards(user_id):
    try:
        script = 'SELECT card_number, card_expiry, encrypted_card_number FROM cards WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        cards = cur.fetchall()
        return cards
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_all_cards\n" + str(e))

    
def get_card(user_id):
    try:
        script = 'SELECT new_card_number, new_card_expiry FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        row = cur.fetchone()
        return row
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_card\n" + str(e))
        
def authCard(user_id, cardNumber, expiry, encrypted_card_number):
    try:
        script = 'INSERT INTO cards (user_id, card_number, card_expiry, encrypted_card_number) VALUES (%s, %s, %s, %s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id), cardNumber, expiry, encrypted_card_number))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: authCard\n" + str(e))

def set_session_id(user_id, session_id):
    script = 'UPDATE app_users SET session_id=(%s) WHERE user_id=(%s);'
    cur = conn.cursor()
    cur.execute(script, (session_id, str(user_id)))
    conn.commit()

def set_timer_sms(user_id, time):
    try:
        script = 'UPDATE app_users SET expire=(%s) WHERE user_id=(%s); '
        cur = conn.cursor()
        cur.execute(script, (time, user_id))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_timer_sms\n" + str(e))
    
def get_card_from_user_mobile_payment_oper(user_id):
    try:
        script = 'SELECT "FROM_USER_CARD_NUMBER" FROM mobile_payments_report WHERE "FROM_USER_ID"=(%s) ORDER BY "ID" DESC LIMIT 1;'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_amount_from_user_mobile_payment_oper\n" + str(e))
        
def get_to_phone_number_oper(user_id):
    try:
        script = 'SELECT "TO_PHONE_NUMBER" FROM mobile_payments_report WHERE "FROM_USER_ID"=(%s) ORDER BY "ID" DESC LIMIT 1;'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_to_phone_number_oper\n" + str(e))
        
def get_session_id(user_id):
    script = 'SELECT session_id FROM app_users WHERE user_id=(%s);'
    cur = conn.cursor()
    cur.execute(script, (str(user_id),))
    return cur.fetchone()[0]

def get_amount_from_user_mobile_payment_oper(user_id):
    try:
        script = 'SELECT "FROM_USER_AMOUNT" FROM mobile_payments_report WHERE "FROM_USER_ID"=(%s) ORDER BY "ID" DESC LIMIT 1;'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_amount_from_user_mobile_payment_oper\n" + str(e))
        
def set_mobile_payment_from_user_card(id_oper, from_user_card_number):
    try:
        script = 'UPDATE mobile_payments_report SET "FROM_USER_CARD_NUMBER"=(%s) WHERE "ID"=(%s); '
        cur = conn.cursor()
        cur.execute(script, (from_user_card_number, id_oper))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_mobile_payment_from_user_card\n" + str(e))
        
def set_mobile_payment_amount(id_oper, from_user_amount):
    try:
        script = 'UPDATE mobile_payments_report SET "FROM_USER_AMOUNT"=(%s) WHERE "ID"=(%s); '
        cur = conn.cursor()
        cur.execute(script, (from_user_amount, id_oper))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_mobile_payment_amount\n" + str(e))
        
def get_mobile_payment_oper_id(user_id):
    try:
        script = 'SELECT "ID" FROM mobile_payments_report WHERE "FROM_USER_ID"=(%s) ORDER BY "ID" DESC LIMIT 1;'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_mobile_payment_oper_id\n" + str(e))

def set_mobile_payment_oper_id_app_user(user_id, oper_id):
    try:
        script = 'UPDATE app_users SET mobile_payment_oper_id=(%s) WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (oper_id, user_id))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_mobile_payment_oper_id_app_user\n" + str(e))
        
def mobile_payment_report_commit(from_user_id, from_user_name, from_user_surname, to_phone_number, date_time):
    try:
        script = 'INSERT INTO mobile_payments_report ("FROM_USER_ID", "FROM_USER_NAME", "FROM_USER_SURNAME", ' \
                 '"TO_PHONE_NUMBER", "DATE_TIME") VALUES (%s, %s, %s, %s, %s);'
        cur = conn.cursor()
        cur.execute(script, (
            str(from_user_id), from_user_name, from_user_surname, to_phone_number, date_time))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: mobile_payment_report_commit\n" + str(e))
    
def legal_entityAccountTurnover(user_id):
    try:
        script = 'SELECT * FROM "legal_entityAccountTurnover" WHERE phone_number=(SELECT phone_number FROM app_users WHERE user_id=(%s)) AND "codeCoa" LIKE (%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id), '2%'))
        AccountTurnover = cur.fetchall()
        return AccountTurnover
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: AccountTurnover\n" + str(e))
        
def code_branch_atm(code, d):
    try:
        script = 'SELECT "CODE_BRANCH" FROM "ATM_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) AND "CODE_LANG"=(%s));'
        cur = conn.cursor()
        cur.execute(script, (code, d))
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: code_branch\n" + str(e))

def code_branch_b(code, d):
    try:
        script = 'SELECT "CODE_DISCTRICT" FROM "DISTRICTS" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) AND "CODE_LANG"=(%s));'
        cur = conn.cursor()
        cur.execute(script, (code, d))
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: code_branch\n" + str(e))


def get_inline_markup(table, code_lang, name):
    try:
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT url, url_text FROM {} WHERE code_lang=(%s) AND name=("
                            "%s) ORDER BY order_number ASC").format(sql.Identifier(table)), [code_lang, name])
        return cur.fetchall()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: inline_markup\n" + str(e))


def get_reply_markup(code_lang, state_id):
    try:
        script = 'SELECT button FROM markups WHERE code_lang=(%s) AND state_id=(%s) ORDER BY order_number ASC'
        cur = conn.cursor()
        cur.execute(script, (code_lang, state_id))
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_reply_markup\n" + str(e))


def get_state(code_lang, name, table):
    try:
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT name FROM state WHERE id=(SELECT state_id FROM {} WHERE code_lang=(%s) and name=("
                            "%s))").format(sql.Identifier(table)), [code_lang, name])
        return cur.fetchone()[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_state\n" + str(e))


def get_user_state(user_id):
    try:
        script = 'SELECT state FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_user_state\n" + str(e))


def get_buttons(code_lang, table):
    try:
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT name, button_title, title, state_id, url FROM {} WHERE code_lang=(%s) ORDER BY "
                            "order_number ASC").format(sql.Identifier(table)), [code_lang])
        return cur.fetchall()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_buttons\n" + str(e))


def get_poll_url(key, lang):
    try:
        script = 'SELECT field_text FROM app_dictionary WHERE key=(%s) AND code_lang=(%s);'
        cur = conn.cursor()
        cur.execute(script, (key, lang))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_poll_url\n" + str(e))


def get_image(file_name):
    try:
        script = 'SELECT "FILE_ID" FROM "BRANCH_IMAGES" WHERE "FILE_NAME"=(%s);'
        cur = conn.cursor()
        cur.execute(script, (file_name,))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_image\n" + str(e))


def image_insert(file_id, file_name):
    try:
        script = 'INSERT INTO "BRANCH_IMAGES" ("FILE_ID", "FILE_NAME") VALUES (%s, %s);'
        cur = conn.cursor()
        cur.execute(script, (file_id, file_name))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: image_insert\n" + str(e))


def playmobile_insert(user_id, message, date_time):
    try:
        script = 'INSERT INTO playmobile_report ("USER_ID", "MESSAGE", "DATE_TIME") VALUES (%s, %s, %s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id), message, date_time))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: playmobile_insert\n" + str(e))


def set_p2p_oper_id_app_user(user_id, oper_id):
    try:
        script = 'UPDATE app_users SET p2p_report_oper_id=(%s) WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (oper_id, user_id))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_p2p_oper_id\n" + str(e))

def get_to_card_p2p_oper(user_id):
    try:
        script = 'SELECT "TO_CARD_NUMBER" FROM p2p_report WHERE "FROM_USER_ID"=(%s) ORDER BY "ID" DESC LIMIT 1;'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_to_card_p2p_oper\n" + str(e))
        
def get_amount_from_user_p2p_oper(user_id):
    try:
        script = 'SELECT "FROM_USER_AMOUNT" FROM p2p_report WHERE "FROM_USER_ID"=(%s) ORDER BY "ID" DESC LIMIT 1;'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_amount_from_user_p2p_oper_id\n" + str(e))
        
def get_p2p_oper_id(user_id):
    try:
        script = 'SELECT "ID" FROM p2p_report WHERE "FROM_USER_ID"=(%s) ORDER BY "ID" DESC LIMIT 1;'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_p2p_oper_id\n" + str(e))


def set_p2p_info(id_oper, status, details, date_time):
    try:
        script = 'UPDATE p2p_report SET "STATUS"=(%s), "DETAILS"=(%s), "DATE_TIME"=(%s) WHERE "ID"=(%s);'
        cur = conn.cursor()
        cur.execute(script, (status, details, date_time, id_oper))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_p2p_info\n" + str(e))


def set_p2p_from_user_card(id_oper, from_user_card_number):
    try:
        script = 'UPDATE p2p_report SET "FROM_USER_CARD_NUMBER"=(%s) WHERE "ID"=(%s); '
        cur = conn.cursor()
        cur.execute(script, (from_user_card_number, id_oper))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_p2p_from_user_card\n" + str(e))


def set_p2p_amount(id_oper, from_user_amount):
    try:
        script = 'UPDATE p2p_report SET "FROM_USER_AMOUNT"=(%s) WHERE "ID"=(%s); '
        cur = conn.cursor()
        cur.execute(script, (from_user_amount, id_oper))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_p2p_amount\n" + str(e))


def p2p_report_commit(from_user_id, from_user_name, from_user_surname, to_card_number, date_time):
    try:
        script = 'INSERT INTO p2p_report ("FROM_USER_ID", "FROM_USER_NAME", "FROM_USER_SURNAME", ' \
                 '"TO_CARD_NUMBER", "DATE_TIME") VALUES (%s, %s, %s, %s, %s);'
        cur = conn.cursor()
        cur.execute(script, (
            str(from_user_id), from_user_name, from_user_surname, to_card_number, date_time))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: p2p_report_commit\n" + str(e))


def get_user_unique_code(unique_code):
    try:
        script = 'SELECT * FROM "USERS_UNIQUE_CODE" WHERE "UNIQUE_CODE"=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(unique_code),))
        return cur.fetchone() is not None
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_user_unique_code\n" + str(e))


def set_user_unique_code(user_id, aacct, unique_code):
    try:
        script = 'INSERT INTO "USERS_UNIQUE_CODE" ("USER_ID", "AACCT", "UNIQUE_CODE") VALUES (%s, %s, %s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id), aacct, unique_code))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_user_unique_code\n" + str(e))


def get_minibank(region_code, code_lang, code_branch):
    try:
        script = 'SELECT * FROM "MINIBANK" WHERE "FK_ID_MINIBANK_BRANCHES"=(SELECT "ID" FROM "MINIBANK_BRANCHES" ' \
                 'WHERE "NAME"=(' \
                 'SELECT "NAME" FROM "MINIBANK_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE ' \
                 '"CODE"=(' \
                 '%s) AND "CODE_LANG"=(%s)) AND "CODE_BRANCH"=(%s))) '
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang, code_branch))
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_minibank\n" + str(e))


def get_atm(region_code, code_lang, code_branch):
    try:
        script = 'SELECT * FROM "ATM" WHERE "FK_ID_ATM_BRANCHES"=(SELECT "ID" FROM "ATM_BRANCHES" WHERE "NAME"=(' \
                 'SELECT "NAME" FROM "ATM_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(' \
                 '%s) AND "CODE_LANG"=(%s)) AND "CODE_BRANCH"=(%s))) '
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang, code_branch))
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_atm\n" + str(e))


def get_minibank_branch(region_code, code_lang, code_branch):
    try:
        script = 'SELECT "NAME" FROM "MINIBANK_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) ' \
                 'AND "CODE_LANG"=(%s)) AND "CODE_BRANCH"=(%s); '
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang, code_branch))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_minibank_branch\n" + str(e))


def get_atm_branch(region_code, code_lang, code_branch):
    try:
        script = 'SELECT "NAME" FROM "ATM_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) ' \
                 'AND "CODE_LANG"=(%s)) AND "CODE_BRANCH"=(%s); '
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang, code_branch))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_atm_branch\n" + str(e))


def get_branches(region_code, code_lang, code_district):
    try:
        script = 'SELECT * FROM "BRANCHES" WHERE "FK_ID_DISTRICT"=(SELECT "ID" FROM "DISTRICTS" WHERE "NAME"=(SELECT ' \
                 '"NAME" FROM "DISTRICTS" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) AND ' \
                 '"CODE_LANG"=(%s)) AND "CODE_DISCTRICT"=(%s)));'
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang, code_district))
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_branches\n" + str(e))


def get_district(region_code, code_lang, code_district):
    try:
        script = 'SELECT "NAME" FROM "DISTRICTS" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) ' \
                 'AND "CODE_LANG"=(%s)) AND "CODE_DISCTRICT"=(%s); '
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang, code_district))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_district\n" + str(e))

def get_minibanks(region_code, code_lang):
    try:
        script = 'SELECT * FROM "MINIBANK_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(' \
                 '%s) AND "CODE_LANG"=(%s));'
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang))
        regions = cur.fetchall()
        return regions
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_minibanks\n" + str(e))


def get_atms(region_code, code_lang):
    try:
        script = 'SELECT * FROM "ATM_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) AND ' \
                 '"CODE_LANG"=(%s));'
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang))
        regions = cur.fetchall()
        return regions
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_atms\n" + str(e))


def get_districts(region_code, code_lang):
    try:
        script = 'SELECT * FROM "DISTRICTS" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) AND ' \
                 '"CODE_LANG"=(%s));'
        cur = conn.cursor()
        cur.execute(script, (region_code, code_lang))
        regions = cur.fetchall()
        return regions
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_districts\n" + str(e))


def get_region_id(user_id):
    try:
        script = 'SELECT code_region FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (user_id,))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_region_id\n" + str(e))


def get_region(code, lang):
    try:
        script = 'SELECT "NAME" FROM "REGIONS" WHERE "CODE"=(%s) and "CODE_LANG"=(%s);'
        cur = conn.cursor()
        cur.execute(script, (code, lang))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_region\n" + str(e))


def get_regions(code_lang):
    try:
        script = 'SELECT "NAME" FROM "REGIONS" WHERE "CODE_LANG"=(%s);'
        cur = conn.cursor()
        cur.execute(script, (code_lang,))
        regions = cur.fetchall()
        return regions
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_regions\n" + str(e))
        

def code_branch_minibank(code, d):
    try:
        script = 'SELECT "CODE_BRANCH" FROM "MINIBANK_BRANCHES" WHERE "FK_ID_REGION"=(SELECT "ID" FROM "REGIONS" WHERE "CODE"=(%s) AND "CODE_LANG"=(%s));'
        cur = conn.cursor()
        cur.execute(script, (code, d))
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: code_branch_minibank\n" + str(e))


def distinct_regions():
    try:
        script = 'SELECT DISTINCT "CODE" FROM "REGIONS";'
        cur = conn.cursor()
        cur.execute(script)
        branches = cur.fetchall()
        return branches
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: distinct_regions\n" + str(e))


def get_card_json(user_id):
    try:
        script = 'SELECT * FROM cards WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        card_json = cur.fetchall()
        return card_json
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_card_json\n" + str(e))


def get_log(user_id):
    try:
        script = 'SELECT log_text FROM log WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_log\n" + str(e))


def update_log(user_id, log_text):
    try:
        script = "UPDATE log SET log_text=(%s) WHERE user_id=(%s);"
        cur = conn.cursor()
        cur.execute(script, (log_text + "\n", str(user_id)))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: update_log\n" + str(e))


def get_news(lang):
    try:
        script = 'SELECT title FROM news WHERE code_lang=(%s);'
        cur = conn.cursor()
        cur.execute(script, (lang,))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_news\n" + str(e))


def update(user_id, cards):
    try:
        script = 'DELETE FROM cards WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        conn.commit()
        ids = []
        for card in cards:
            in_card = svgate.new_card(card["pan"], card["expiry"])
            if in_card["result"]:
                insert_script = 'INSERT INTO cards(user_id, card_json, aacct, mfo, client_unique_id) VALUES (%s, %s, %s, %s, %s);'
                cur = conn.cursor()
                cur.execute(insert_script, (str(user_id), json.dumps(in_card), (in_card["result"]["aacct"])[5:], (in_card["result"]["aacct"])[0:5], (in_card["result"]["aacct"])[-11:-3]))
                ids.append(str(in_card["result"]['id']))
        conn.commit()
        return svgate.get_balance(ids)
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: update\n" + str(e))


def set_log(user_id, phone_number):
    try:
        script = 'INSERT INTO log (user_id, phone_number, log_text) VALUES (%s, %s, %s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id), phone_number, '**** START ****'))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_log\n" + str(e))


def get_phone_number(user_id):
    try:
        script = 'SELECT phone_number FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_phone_number\n" + str(e))


def get_code(user_id):
    try:
        script = 'SELECT code_otp FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_code\n" + str(e))


def set_code(user_id, code):
    try:
        script = 'UPDATE app_users SET code_otp=(%s) WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (code, str(user_id)))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_code\n" + str(e))


def set_phone_number(user_id, phone_number):
    try:
        script = 'UPDATE app_users SET phone_number=(%s) WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (phone_number, str(user_id)))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_phone_number\n" + str(e))


def get_lang(user_id):
    try:
        script = 'SELECT user_language FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_lang\n" + str(e))


def set_lang(user_id, lang):
    try:
        script = 'UPDATE app_users SET user_language=(%s) WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (lang, str(user_id)))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_lang\n" + str(e))


def get_dict(key, lang):
    try:
        script = 'SELECT field_text FROM app_dictionary WHERE key=(%s) and code_lang=(%s);'
        cur = conn.cursor()
        cur.execute(script, (key, lang))
        row = cur.fetchone()
        return row[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_dict\n" + str(e))


def set_user_state(user_id, state):
    try:
        script = 'UPDATE app_users SET state=(%s) WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (state, str(user_id)))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: set_user_state\n" + str(e))


def get_user(user_id):
    try:
        script = 'SELECT * FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_user\n" + str(e))


def get_user_status(user_id):
    try:
        script = 'SELECT status FROM app_users WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id),))
        return cur.fetchone()[0]
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: get_user_status\n" + str(e))

def update_user_status(user_id):
    try:
        script = 'UPDATE app_users SET status=(%s) WHERE user_id=(%s);'
        cur = conn.cursor()
        cur.execute(script, ('1', str(user_id)))
        conn.commit()
    except(Exception, Error) as e:
        logger_app.error("/database_connection/dbcon.py\nMethod: update_user_status\n" + str(e))

def add_user(user_id, phone_number, first_name, last_name, username, state):
    try:
        script = 'INSERT INTO app_users (user_id, phone_number, first_name, last_name, username, user_language, ' \
                 'state, code_otp, status, expire) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        cur = conn.cursor()
        cur.execute(script, (str(user_id), phone_number, first_name, last_name, username, 'ru', state, None, '0', str(dt.datetime.now())))
        conn.commit()
    except(Exception, Error) as e:
        print(e)
