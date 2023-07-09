from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keys_token import tokens



storage = MemoryStorage()
bot = Bot(token = tokens.tgtoken())
dp = Dispatcher(bot, storage = storage)
