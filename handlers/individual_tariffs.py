from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import get_user_state


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_INDIVIDUAL_TARIFFS)
async def individual_tariffs(message: types.Message):
    await markups.get_markups('individual_tariffs', message)
