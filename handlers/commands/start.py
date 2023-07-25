from aiogram import types

from bot_tg.loader import dp, bot
from buttons.reply import menu_main


@dp.message_handler(commands=['start'], state="*")
async def start_cmd(message: types.Message) -> None:
    await bot.send_message(
        chat_id=message.chat.id,
        text="Привет, это бот в котором ты сможешь записаться на встречу",
        parse_mode='html',
        reply_markup=menu_main
        )
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print("Ошибка при удалении сообщения:", e)
