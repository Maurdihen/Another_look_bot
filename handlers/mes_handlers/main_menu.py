import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_tg.loader import dp, bot
from buttons.inlines import general_info_markup


@dp.message_handler(lambda message: message.text == "Общая информация")
async def general_inf(message: types.Message):
    await asyncio.sleep(0.5)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print("Ошибка при удалении сообщения:", e)

    await bot.send_message(
        chat_id=message.chat.id,
        text="Тут какая-то общая информация",
        parse_mode='html',
        reply_markup=general_info_markup
    )


@dp.message_handler(lambda message: message.text == "Мои записи", state="*")
async def my_notes(message: types.Message):
    await asyncio.sleep(0.5)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print("Ошибка при удалении сообщения:", e)

    await bot.send_message(
        chat_id=message.chat.id,
        text="Тут будут мои записи списком с возможностью листать при помощи стрелки",
        parse_mode='html',
        reply_markup=general_info_markup
    )



