from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_LEGAL_ACCEPTING_PAYMENT)
async def legal_accepting_payment(message: types.Message):
    await markups.get_markups('legal_accepting_payment', message)
