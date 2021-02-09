from aiogram import executor
from misc import dp


while True:
    try:
        import handlers
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        print('Restart')


