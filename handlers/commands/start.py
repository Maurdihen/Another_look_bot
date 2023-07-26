from aiogram.types import Message

from bot_tg.loader import dp, bot


@dp.message_handler(commands=['start'], state="*")
async def start_cmd(message: Message) -> None:
    await bot.send_message(chat_id=message.chat.id, text="Hello", parse_mode='html')