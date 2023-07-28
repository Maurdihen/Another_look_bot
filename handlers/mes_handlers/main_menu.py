import asyncio

from aiogram import types

from bot_tg.loader import dp, bot
from buttons.inlines import general_info_markup

from db_work.setup_db import session
from db_work.service.notes_service import NotesService
from db_work.service.users_service import UsersService


users_service = UsersService(session)
notes_service = NotesService(session)


@dp.message_handler(lambda message: message.text == "Записаться")
async def general_inf(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print("Ошибка при удалении сообщения:", e)

    await bot.send_message(
        chat_id=message.chat.id,
        text="Ты хочешь индивидуальную консультацию или тематический курс /мастер-класс? Выбирай 🔽🔽🔽",
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
        type_of_meeting = note.category
        if note.subcategory:
            type_of_meeting += ", " + note.subcategory

        info = f"Тип встречи: {type_of_meeting}\n" \
               f"День встречи: {note.date}\n" \
               f"Время встречи: {note.time}" \

        list_user_notes.append(({"note_id": note.id}, info))

    await bot.send_message(
        chat_id=message.chat.id,
        text=list_user_notes,
        parse_mode='html'
    )


@dp.message_handler(content_types=['contact'])
async def my_number(message: types.Message):
    print(message.contact)
