from aiogram import Bot, Dispatcher, types
from config import TOKEN, PROXY_URL
from datetime import date
import logging
from logging.handlers import TimedRotatingFileHandler
import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    asyncio.set_event_loop(asyncio.SelectorEventLoop())

date = date.today().strftime("%Y.%m.%d")

log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = 10

# APP logger
logname_app = "app.log"
handler_app = TimedRotatingFileHandler(filename="C:/#root/Projects/hb_telebot_new/Log/APP_LOG/"+logname_app, when="midnight", interval=1)
handler_app.suffix = "%d%m%Y"
handler_app.setLevel(log_level)
formatter = logging.Formatter(log_format)
handler_app.setFormatter(formatter)
logger_app = logging.getLogger(__name__)
logger_app.addHandler(handler_app)

# P2P logger
logname_p2p = "p2p.log"
handler_p2p = TimedRotatingFileHandler(filename="C:/#root/Projects/hb_telebot_new/Log/P2P_LOG/"+logname_p2p, when="midnight", interval=1)
handler_p2p.suffix = "%d%m%Y"
handler_p2p.setLevel(log_level)
formatter = logging.Formatter(log_format)
handler_p2p.setFormatter(formatter)
logger_p2p = logging.getLogger(__name__)
logger_p2p.addHandler(handler_p2p)


bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
