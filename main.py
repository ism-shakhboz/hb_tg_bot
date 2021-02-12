from aiogram import executor
from misc import dp
from misc import config
from database_connection.dbcon import conn
from api import send_request_playmobile


def sms_attention():
    script = 'SELECT "ID" FROM playmobile_report order by "ID" DESC LIMIT 1'
    cur = conn.cursor()
    cur.execute(script)
    sms_load = {
        "messages":
            [
                {
                    "recipient": config['SMS_ATTENTION']['phone_number'],
                    "message-id": int(cur.fetchone()[0]) + 1,
                    "sms": {
                        "originator": "3500",
                        "content": {
                            "text": "Bot ishida muammo yuzaga keldi"
                        }
                    }
                }
            ]
    }
    send_request_playmobile(sms_load)


i = 0
if __name__ == '__main__':
    while True:
        try:
            import handlers

            executor.start_polling(dp, skip_updates=True)
        except Exception as e:
            i = i + 1
            print('Идет попытка повторного запуска: ')
            if i > 5:
                sms_attention()
                break
