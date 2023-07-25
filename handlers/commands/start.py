from aiogram import types
from sqlalchemy.exc import NoResultFound

from bot_tg.loader import dp, bot
from buttons.reply import menu_main

from bd.model import session, Users


@dp.message_handler(commands=['start'], state="*")
async def start_cmd(message: types.Message) -> None:
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    if user_last_name:
        user_name = f"{user_first_name} {user_last_name}"
    else:
        user_name = user_first_name


    try:
        existing_user = session.query(Users).filter_by(user_id=message.from_user.id).first()

        if not existing_user:
            new_user = Users(user_id=message.from_user.id, name=user_name)
            session.add(new_user)
            session.commit()

    except NoResultFound:
        new_user = Users(user_id=message.from_user.id, name=user_name)
        session.add(new_user)
        session.commit()

    finally:
        session.close()

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
