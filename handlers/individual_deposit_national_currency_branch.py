from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *

@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_CONTRIBUTION_NATIONAL_CURRENCY_BRANCHES)
async def individual_deposit_national_currency_branch(message: types.Message):
    await markups.get_markups('individual_deposit_national_currency_branch', message)
