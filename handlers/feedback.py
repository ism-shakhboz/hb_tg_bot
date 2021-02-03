from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_FEEDBACK)
async def feedback(message: types.Message):
    await markups.get_markups('feedback', message)
