from aiogram import types

from aiogram.dispatcher import FSMContext

from bot_tg.loader import dp, bot
from buttons.inlines import create_look_slots
from states import UserStates

@dp.message_handler(commands=['admin'], state="*")
async def admin_cmd(message: types.Message, state: FSMContext) -> None:
    print(message.from_user.id)
    if message.from_user.id == 1362055393:
        await bot.send_message(message.chat.id, "Привет женя, это твоя админка", reply_markup=create_look_slots)
        await UserStates.Admin.set()
    else:
        await bot.send_message(message.chat.id, "Сори ты не админ")
