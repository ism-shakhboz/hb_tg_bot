from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_MONEY_TRANSFER'))
async def individual_money_transfer(message: types.Message):
    await markups.get_markups('individual_money_transfer', message)
