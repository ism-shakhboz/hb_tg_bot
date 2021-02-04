from misc import dp, bot, logger_app
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *
import requests
import uuid

payload = {

          "username": "batirov",
          "password": "bank_09012+-"
    }

def send_get_token(payload):
    r = requests.post('http://10.12.16.76:7079/getToken', json=payload).json()
    return r


def send_get_accountTurnOver(accountTurnover):
    
    r = requests.get('http://10.12.16.76:7079/1.0.0/accountTurnover/'+accountTurnover[5]+'?codeCoa='+accountTurnover[2]+'&filialCode='+accountTurnover[3]+'&accExternal='+accountTurnover[4]+'&clientCode='+accountTurnover[6]+'', headers={'content-type': 'application/json', 'Authorization':'Bearer '+send_get_token(payload)['token'], 'requestId': str(uuid.uuid4())}).json()
    
    return r

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_BALANCE_OPER)
async def legal_entity_bills(message: types.Message):
    try:
        user_id = message.from_user.id
        d = get_lang(user_id)
        update_log(user_id, get_log(user_id) + message.text)
        if message.text == get_dict('back', d):
            await bot.send_message(user_id, get_dict('legal_entity_hint', d), reply_markup=markups.legal_entity(d))
            User().set_user_state(user_id, states.S_LEGAL_ENTITY)
        elif message.text == get_dict('main_menu', d):
            await bot.send_message(user_id, get_dict('main_menu_hint', d), reply_markup=markups.main_menu(d))
            User().set_user_state(user_id, states.S_GET_MAIN_MENU)
        elif message.text == get_dict('balance_state', d):
            str_get = ''
            #accountTurnover = legal_entityAccountTurnover(163302497)
            accountTurnover = legal_entityAccountTurnover(user_id)
            
            if len(accountTurnover)>0:
                for i in range(len(accountTurnover)):
                    resp = send_get_accountTurnOver(accountTurnover[i])
                    
                    saldoOut = (("{:,}".format(int(resp['responseBody']['saldoOut'])/100)).replace(',', ' '))
                    name = resp['responseBody']['name']
                    accExternal = resp['responseBody']['accExternal']
                    str_get = str_get + '\n' + name[:80] + '\n' + accExternal + '\n' + get_dict('remainder', d) + ' ' +saldoOut + ' '+get_dict('sum', d)+'\n'
                await bot.send_message(user_id, get_dict('account_status_message', d)+'\n'+str_get)
            else:
                await bot.send_message(user_id, get_dict('no_ext_account', d))
        elif message.text == get_dict('cardindex_1', d):
            k1 = 'SELECT * FROM "legal_entityAccountTurnover" WHERE phone_number=(SELECT phone_number FROM app_users WHERE user_id=(%s)) AND "codeCoa"=(%s);'
            cur = conn.cursor()
            cur.execute(k1, (str(user_id), '96319'))
            accountTurnover = cur.fetchall()
            str_get = ''
            if len(accountTurnover)>0:
                for i in range(len(accountTurnover)):
                    resp = send_get_accountTurnOver(accountTurnover[i])
                    saldoOut = (("{:,}".format(int(resp['responseBody']['saldoOut'])/100)).replace(',', ' '))
                    name = resp['responseBody']['name']
                    accExternal = resp['responseBody']['accExternal']
                    str_get = str_get + '\n' + name[:80] + '\n' + accExternal + '\n' + get_dict('remainder', d) + ' ' +saldoOut + ' '+get_dict('sum', d)+'\n'
                await bot.send_message(user_id, get_dict('account_status_message', d)+'\n'+str_get)
            else:
                await bot.send_message(user_id, get_dict('no_ext_account', d))
        elif message.text == get_dict('cardindex_2', d):
            k2 = 'SELECT * FROM "legal_entityAccountTurnover" WHERE phone_number=(SELECT phone_number FROM app_users WHERE user_id=(%s)) AND "codeCoa"=(%s);'
            cur = conn.cursor()
            cur.execute(k2, (str(user_id), '96321'))
            accountTurnover = cur.fetchall()
            str_get = ''
            if len(accountTurnover)>0:
                for i in range(len(accountTurnover)):
                    resp = send_get_accountTurnOver(accountTurnover[i])
                    saldoOut = (("{:,}".format(int(resp['responseBody']['saldoOut'])/100)).replace(',', ' '))
                    name = resp['responseBody']['name']
                    accExternal = resp['responseBody']['accExternal']
                    str_get = str_get + '\n' + name[:80] + '\n' + accExternal + '\n' + get_dict('remainder', d) + ' ' +saldoOut + ' '+get_dict('sum', d)+'\n'
                await bot.send_message(user_id, get_dict('account_status_message', d)+'\n'+str_get)
            else:
                await bot.send_message(user_id, get_dict('no_ext_account', d))
    except Exception as e:
        logger_app.error("/handlers/legal_entity_bills.py\nMethod: legal_entity_bills\n"+str(e))
