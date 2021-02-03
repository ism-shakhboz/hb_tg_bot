from misc import dp
from aiogram import types
from vars import states, markups
from database_connection.dbcon import *


@dp.message_handler(lambda message: get_user_state(message.from_user.id) == states.S_LOAN_LEGAL_ENTITY)
async def legal_entity_loan(message: types.Message):
    await markups.get_markups('legal_loans', message)