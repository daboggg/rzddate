import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.handlers.user_hendlers import register_handler

load_dotenv()
token = os.getenv('TOKEN_API')
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_handler(dp)


executor.start_polling(dp, skip_updates=True)

