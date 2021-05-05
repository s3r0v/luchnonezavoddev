import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage

from bot.config import TOKEN


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
storage = JSONStorage("states.json")
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
