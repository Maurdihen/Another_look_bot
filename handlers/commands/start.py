from aiogram.types import Message
from aiogram.dispatcher.filters import CommandStart

from bot_tg.loader import dp, bot


@dp.message_handler(commands=CommandStart(), state="*")
async def start_cmd(message: Message) -> None:
    await bot.send_message(chat_id=message.chat.id, text="Hello", parse_mode='html')