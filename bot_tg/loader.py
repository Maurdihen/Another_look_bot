from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_config import BotConfig

bot = Bot(token=BotConfig.dev_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())