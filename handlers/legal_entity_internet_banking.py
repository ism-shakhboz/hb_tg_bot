from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == get_state_by_key('S_LEGAL_ENTITY_INTERNET_BANKING'))
async def legal_internet_banking(message: types.Message):
    await markups.get_markups('legal_internet_banking', message)
