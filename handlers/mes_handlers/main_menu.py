import asyncio

from aiogram import types

from bot_tg.loader import dp, bot
from buttons.inlines import general_info_markup
from db.dao.model.model import session
from db.service.notes_service import NotesService
from db.service.users_service import UsersService


users_service = UsersService(session)
notes_service = NotesService(session)


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

    user = users_service.get_user_by_tg_id(message.from_user.id)

    user_notes = user.notes
    list_user_notes = []
    for note in user_notes:
        list_user_notes.append(f"Note ID: {note.id}, Date: {note.date}, Time: {note.time}, Category: {note.category}, Sub-category: {note.sub_category}")

    await bot.send_message(
        chat_id=message.chat.id,
        text=list_user_notes,
        parse_mode='html'
    )
