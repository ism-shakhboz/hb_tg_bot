from config import url, terminalId, merchantId, port, headers, url_pm, login_pm, password_pm
import requests
import json
import configparser
from requests.auth import HTTPBasicAuth
import datetime as dt
import pytz
import uuid
import urllib.request
from misc import logger_app
from random import randint

proxies = {
       
        "http":"http://10.12.16.202:8081"
    }
headers['Content-Type'] = 'application/json'

def send_request(payload):
    try:
        request = urllib.request.Request(url)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(payload)
        jsondataasbytes = jsondata.encode('utf-8')
        request.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(request, jsondataasbytes)
        resp = json.loads(response.read().decode('utf8'))
        return resp
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: send_request_playmobile\n"+str(e))

'''
def send_request(payload):
    try:
        response = requests.post(url, json=payload).json()
        print(type(response))
        return response
    except Exception as e:
        print(e)
'''

def send_request_playmobile(sms_load):
    try:
        response = requests.post(url_pm, json=sms_load, auth=HTTPBasicAuth(login_pm, password_pm), headers=headers)
        return response
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: send_request_playmobile\n"+str(e))

def authCard(card, expiry):
    try:
        tz = pytz.utc.localize(dt.datetime.utcnow())
        payload = {
                "msgid": str(uuid.uuid4()),
                "msgcorrid": str(uuid.uuid4()),
                "msgdate": str(dt.datetime.utcnow().isoformat(sep='T', timespec='milliseconds'))+'+05:00',
                "msgmode": "SYNCHRONOUS",
                "msgtype": "REQUEST",
                "msgresptype": "JSON",
                "msgsource": "TlgBot",
                "msgmethod": "TlgBot.authCard",
                "msgmethodparams":  {
                      "card": card,
                      "expiry": expiry
                    }
                }
        resp = send_request(payload)
        return resp
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: authCard\n"+str(e))


def payP2p(from_card, expiry, to_card, amount):
    try:
        tz = pytz.utc.localize(dt.datetime.utcnow())
        payload = {
                "msgid": str(uuid.uuid4()),
                "msgcorrid": str(uuid.uuid4()),
                "msgdate": str(dt.datetime.utcnow().isoformat(sep='T', timespec='milliseconds'))+'+05:00',
                "msgmode": "SYNCHRONOUS",
                "msgtype": "REQUEST",
                "msgresptype": "JSON",
                "msgsource": "TlgBot",
                "msgmethod": "TlgBot.payP2p",
                "msgmethodparams":  {
                    "fromCard": from_card,
                     "expiry": expiry,
                     "toCard": to_card,
                     "amount": amount
                    }
                }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: authCard\n"+str(e))


def getCardName(card_number):
    try:
        tz = pytz.utc.localize(dt.datetime.utcnow())
        payload = {
                "msgid": str(uuid.uuid4()),
                "msgcorrid": str(uuid.uuid4()),
                "msgdate": str(dt.datetime.utcnow().isoformat(sep='T', timespec='milliseconds'))+'+05:00',
                "msgmode": "SYNCHRONOUS",
                "msgtype": "REQUEST",
                "msgresptype": "JSON",
                "msgsource": "TlgBot",
                "msgmethod": "TlgBot.getCardName",
                "msgmethodparams":  {
                    "number": card_number
                    }
                }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: authCard\n"+str(e))

def payCellular(card, expiry, phone, amount):
    try:
        tz = pytz.utc.localize(dt.datetime.utcnow())
        payload = {
                "msgid": str(uuid.uuid4()),
                "msgcorrid": str(uuid.uuid4()),
                "msgdate": str(dt.datetime.utcnow().isoformat(sep='T', timespec='milliseconds'))+'+05:00',
                "msgmode": "SYNCHRONOUS",
                "msgtype": "REQUEST",
                "msgresptype": "JSON",
                "msgsource": "TlgBot",
                "msgmethod": "TlgBot.payCellular",
                "msgmethodparams":  {
                      "card": card,
                      "expiry": expiry,
                      "phone": phone,
                      "amount": amount
                    }
                }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: payCellular\n"+str(e))

def confirmOperationAuthCard(sessionId, confirmCode):
    try:
        tz = pytz.utc.localize(dt.datetime.utcnow())
        payload = {
                "msgid": str(uuid.uuid4()),
                "msgcorrid": str(uuid.uuid4()),
                "msgdate": str(dt.datetime.utcnow().isoformat(sep='T', timespec='milliseconds'))+'+05:00',
                "msgmode": "SYNCHRONOUS",
                "msgtype": "REQUEST",
                "msgresptype": "JSON",
                "msgsource": "TlgBot",
                "msgmethod": "TlgBot.confirmOperation",
                "msgmethodparams":  {
                      "sessionId": sessionId,
                      "confirmCode": confirmCode
                    }
                }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: confirmOperation\n"+str(e))


def getCardBalance(card, expiry):
    try:
        tz = pytz.utc.localize(dt.datetime.utcnow())
        payload = {
                "msgid": str(uuid.uuid4()),
                "msgcorrid": str(uuid.uuid4()),
                "msgdate": str(dt.datetime.utcnow().isoformat(sep='T', timespec='milliseconds'))+'+05:00',
                "msgmode": "SYNCHRONOUS",
                "msgtype": "REQUEST",
                "msgresptype": "JSON",
                "msgsource": "TlgBot",
                "msgmethod": "TlgBot.getCardBalance",
                "msgmethodparams":  {
                      "card": card,
                      "expiry": expiry
                    }
                }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: getCardBalance\n"+str(e))


def get_cards_by_ids(ids):
    try:
        payload = {
            "method": "cards.get",
            "params": {"ids": [ids]},
            "jsonrpc": "2.0",
            "id": 0,
        }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: get_cards\n"+str(e))


def get_sms(phone, code, message_id):
    try:
        phone = phone.replace('+', '')
        sms_load = {
            "messages":
                [
                    {
                        "recipient": phone,
                        "message-id": message_id,
                        "sms": {

                            "originator": "3500",
                            "content": {
                                "text": "Kod aktivasii karti, Vnimaniye!!! Nikomu ne soobshayte kod: %s" % str(code)
                            }
                        }
                    }
                ]
        }
        
        return send_request_playmobile(sms_load)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: get_sms\n"+str(e))


def get_cards(phone):
    try:
        phone = phone.replace('+', '')
        payload = {
            "method": "cards.list",
            "params": {"phone": phone},
            "jsonrpc": "2.0",
            "id": 0,
        }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: get_cards\n"+str(e))


def new_card(pan, expiry):
    try:
        payload = {
            "method": "cards.new",
            "params": {"card": {"pan": pan, "expiry": expiry}},
            "jsonrpc": "2.0",
            "id": 0,
        }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: new_card\n"+str(e))


def p2p_id2pan(token, pan, panexp, amount):
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "p2p.id2pan",
            "id": 123,
            "params":
                {
                    "p2p": {
                        "amount": amount,
                        "date12": "",
                        "ext": str(uuid.uuid4()),
                        "merchantId": merchantId,
                        "port": 1234,
                        "stan": "123456",
                        "terminalId": terminalId,
                        "cardId": token,
                        "recipient": {
                            "pan": pan,
                            "expiry": panexp
                        }
                    }
                }
        }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: p2p_id2pan\n"+str(e))


def p2p_info(pan):
    try:
        payload = {"jsonrpc": "2.0", "method": "p2p.info", "id": 123, "params": {"hpan": pan}}
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: p2p_info\n"+str(e))


def get_balance(ids):
    try:
        payload = {
            "method": "cards.get",
            "params": {"ids": ids},
            "jsonrpc": "2.0",
            "id": 0,
        }
        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: get_balance\n"+str(e))


def get_history(ids, begindate="", enddate=""):
    begindate = (dt.datetime.now() - dt.timedelta(days=15)).strftime("%Y%m%d")
    enddate = dt.datetime.now().strftime("%Y%m%d")
    payload = {
            "method": "trans.history",
            "params": {
                "criteria":
                    {
                        "cardIds": ids,
                        "range":
                            {
                                "startDate": begindate,
                                "endDate": enddate
                            },
                        "pageNumber": 15,
                        "pageSize": 100
                    },

            },
            "jsonrpc": "2.0",
            "id": 0}
    return send_request(payload)


def card_status_change(card_id, status_id):
    try:
        payload = {
            "id": 123,
            "jsonrpc": "2.0",
            "method": "card.status.change",
            "params":
                {
                    "card":
                        {
                            "cardId": card_id,
                            "terminalId": terminalId,
                            "merchantId": merchantId,
                            "port": "1234",
                            "stan": "123456",
                            "ext": str(uuid.uuid4()),
                            "statusId": status_id
                        }
                }
        }

        return send_request(payload)
    except Exception as e:
        logger_app.error("/handlers/svgate.py\nMethod: card_status_change\n"+str(e))
