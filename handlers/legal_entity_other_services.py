from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import get_user_state

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_OTHER_SERVICES)
async def legal_other_services(message: types.Message):
    await markups.get_markups('legal_other_services', message)
