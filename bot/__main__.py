from aiogram import executor
from bot.bot import dispatcher

if __name__ == "__main__":
    executor.start_polling(dispatcher=dispatcher, skip_updates=True)
    
