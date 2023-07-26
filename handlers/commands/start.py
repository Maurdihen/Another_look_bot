from aiogram import types
from sqlalchemy.exc import NoResultFound

from bot_tg.loader import dp, bot
from buttons.reply import menu_main

from db_work.dao.models.model import session
from db_work.service.users_service import UsersService

users_service = UsersService(session)


@dp.message_handler(commands=['start'], state="*")
async def start_cmd(message: types.Message) -> None:
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    if user_last_name:
        user_name = f"{user_first_name} {user_last_name}"
    else:
        user_name = user_first_name

    try:
        existing_user = users_service.get_user_by_tg_id(message.from_user.id)

        if not existing_user:
            users_service.create_user(user_id_tg=message.from_user.id, name=user_name)

    except NoResultFound:
        users_service.create_user(user_id_tg=message.from_user.id, name=user_name)

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
