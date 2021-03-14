import requests
import json
from requests.auth import HTTPBasicAuth
import datetime as dt
import pytz
import uuid
import urllib.request
from misc import logger_app
from misc import config


proxies = {
        "http":config['PROXY']['url']
    }


headers = {'Content-Type': 'application/json'}


def send_request(payload):
    try:
        request = urllib.request.Request(config['API']['url'])
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(payload)
        jsondataasbytes = jsondata.encode('utf-8')
        request.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(request, jsondataasbytes)
        resp = json.loads(response.read().decode('utf8'))
        return resp
    except Exception as e:
        logger_app.error("/handlers/api.py\nMethod: send_request_playmobile\n"+str(e))

def send_request_playmobile(sms_load):
    try:
        response = requests.post(config['PLAY_MOBILE']['url'], json=sms_load, auth=HTTPBasicAuth(config['PLAY_MOBILE']['login'], config['PLAY_MOBILE']['password']), headers=headers)
        return response
    except Exception as e:
        logger_app.error("/handlers/api.py\nMethod: send_request_playmobile\n"+str(e))

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
        logger_app.error("/handlers/api.py\nMethod: authCard\n"+str(e))


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
        logger_app.error("/handlers/api.py\nMethod: authCard\n"+str(e))


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
        logger_app.error("/handlers/api.py\nMethod: authCard\n"+str(e))

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
        logger_app.error("/handlers/api.py\nMethod: payCellular\n"+str(e))

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
        logger_app.error("/handlers/api.py\nMethod: confirmOperation\n"+str(e))


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
        logger_app.error("/handlers/api.py\nMethod: getCardBalance\n"+str(e))


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
        logger_app.error("/handlers/api.py\nMethod: get_sms\n"+str(e))

