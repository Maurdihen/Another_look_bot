from aiogram import types
from sqlalchemy.exc import NoResultFound

from bot_tg.loader import dp, bot
from buttons.inlines import general_info_markup
from buttons.reply import menu_main

from setup_db.sqlite_db import session
from db_work.service.users_service import UsersService
from states import UserStates

from aiogram.dispatcher import FSMContext

users_service = UsersService(session)


@dp.message_handler(commands=['start'], state="*")
async def start_cmd(message: types.Message, state: FSMContext) -> None:
    await state.reset_state()
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print("Ошибка при удалении сообщения:", e)

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
        text="Привет! Это бот центра  психологии и развития молодежи «Другой взгляд» 👋\n"
             "Здесь ты можешь записаться на индивидуальную консультацию к психологу или на тематический курс 📝",
        parse_mode='html',
        reply_markup=menu_main
    )


@dp.message_handler(commands=['admin'], state="*")
async def admin_cmd(message: types.Message, state: FSMContext) -> None:
    print(message.from_user.id)
    if message.from_user.id == 1362055393:
        await bot.send_message(message.chat.id, "Привет женя, это твоя админка", reply_markup=general_info_markup)
        await UserStates.Admin.set()
    else:
        await bot.send_message(message.chat.id, "Сори ты не админ")
