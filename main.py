from aiogram import executor
from misc import dp


i = 0
while True:
    try:
        import handlers
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        if i < 1:
            i = i + 1
