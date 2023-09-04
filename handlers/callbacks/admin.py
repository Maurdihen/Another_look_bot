from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram_calendar import SimpleCalendar, simple_cal_callback

from bot_tg.loader import dp, bot
from buttons.inlines import choose_time, cd, general_info_markup_admin, free_occupied_slots
from states import UserStates


@dp.callback_query_handler(cd.filter(action='create_slots'), state=UserStates.Admin)
async def create_slots_callback_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Выбери какой тип встречи ты хочешь добавить",
                           reply_markup=general_info_markup_admin)


@dp.callback_query_handler(cd.filter(action='look_slots'), state=UserStates.Admin)
async def look_slots_callback_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Выбери что ты хочешь сделать, посмотреть все созданные "
                                                        "тобой ивенты на которые никто не записался и возможно "
                                                        "удалить их, или посмотреть всю информацию о слотах "
                                                        "на которые уже записались",
                           reply_markup=free_occupied_slots)


@dp.callback_query_handler(cd.filter(action='free_slots'), state=UserStates.Admin)
async def free_slots_callback_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Тут будет вывод всех свободных слотов")


@dp.callback_query_handler(cd.filter(action='occupied_slots'), state=UserStates.Admin)
async def occupied_slots_callback_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Тут будет вывод всех занятых слотов")


@dp.callback_query_handler(lambda c: c.data.startswith('admin_'), state=UserStates.Admin)
async def ind_cons_callback_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data["admin_cons"] = callback_query.data.split('_')[1]

    await bot.send_message(
        callback_query.from_user.id,
        "В какой день хочешь добавить, изменить встречу",
        reply_markup=await SimpleCalendar().start_calendar()
    )


@dp.callback_query_handler(simple_cal_callback.filter(), state=UserStates.Admin)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data["date_admin"] = date.strftime("%d/%m/%Y")
        await bot.send_message(
            callback_query.from_user.id,
            'Теперь выбери время'
        )
        await bot.send_message(callback_query.from_user.id, "8️⃣:0️⃣0️⃣", reply_markup=choose_time)


@dp.callback_query_handler(lambda c: c.data.startswith('choose_'), state=UserStates.Admin)
async def choose_time_callback(callback_query: types.CallbackQuery, state: FSMContext):
    time_list = [
        "8️⃣:0️⃣0️⃣", "8️⃣:3️⃣0️⃣",
        "9️⃣:0️⃣0️⃣", "9️⃣:3️⃣0️⃣",
        "1️⃣0️⃣:0️⃣0️⃣", "1️⃣0️⃣:3️⃣0️⃣",
        "1️⃣1️⃣:0️⃣0️⃣", "1️⃣1️⃣:3️⃣0️⃣",
        "1️⃣2️⃣:0️⃣0️⃣", "1️⃣2️⃣:3️⃣0️⃣",
        "1️⃣3️⃣:0️⃣0️⃣", "1️⃣3️⃣:3️⃣0️⃣",
        "1️⃣4️⃣:0️⃣0️⃣", "1️⃣4️⃣:3️⃣0️⃣",
        "1️⃣5️⃣:0️⃣0️⃣", "1️⃣5️⃣:3️⃣0️⃣",
        "1️⃣6️⃣:0️⃣0️⃣", "1️⃣6️⃣:3️⃣0️⃣",
        "1️⃣7️⃣:0️⃣0️⃣", "1️⃣7️⃣:3️⃣0️⃣",
        "1️⃣8️⃣:0️⃣0️⃣", "1️⃣8️⃣:3️⃣0️⃣",
        "1️⃣9️⃣:0️⃣0️⃣", "1️⃣9️⃣:3️⃣0️⃣",
        "2️⃣0️⃣:0️⃣0️⃣", "2️⃣0️⃣:3️⃣0️⃣",
        "2️⃣1️⃣:0️⃣0️⃣"
    ]
    time_dict = {
        "8️⃣:0️⃣0️⃣": "08:00", "8️⃣:3️⃣0️⃣": "08:30",
        "9️⃣:0️⃣0️⃣": "09:00", "9️⃣:3️⃣0️⃣": "09:30",
        "1️⃣0️⃣:0️⃣0️⃣": "10:00", "1️⃣0️⃣:3️⃣0️⃣": "10:30",
        "1️⃣1️⃣:0️⃣0️⃣": "11:00", "1️⃣1️⃣:3️⃣0️⃣": "11:30",
        "1️⃣2️⃣:0️⃣0️⃣": "12:00", "1️⃣2️⃣:3️⃣0️⃣": "12:30",
        "1️⃣3️⃣:0️⃣0️⃣": "13:00", "1️⃣3️⃣:3️⃣0️⃣": "13:30",
        "1️⃣4️⃣:0️⃣0️⃣": "14:00", "1️⃣4️⃣:3️⃣0️⃣": "14:30",
        "1️⃣5️⃣:0️⃣0️⃣": "15:00", "1️⃣5️⃣:3️⃣0️⃣": "15:30",
        "1️⃣6️⃣:0️⃣0️⃣": "16:00", "1️⃣6️⃣:3️⃣0️⃣": "16:30",
        "1️⃣7️⃣:0️⃣0️⃣": "17:00", "1️⃣7️⃣:3️⃣0️⃣": "17:30",
        "1️⃣8️⃣:0️⃣0️⃣": "18:00", "1️⃣8️⃣:3️⃣0️⃣": "18:30",
        "1️⃣9️⃣:0️⃣0️⃣": "19:00", "1️⃣9️⃣:3️⃣0️⃣": "19:30",
        "2️⃣0️⃣:0️⃣0️⃣": "20:00", "2️⃣0️⃣:3️⃣0️⃣": "20:30",
        "2️⃣1️⃣:0️⃣0️⃣": "21:00"
    }

    message_number = int(callback_query.data.split('_')[1])
    if callback_query.data.split('_')[2] == "choose":
        async with state.proxy() as data:
            date = data["date_admin"]
            data["time_admin"] = time_dict[time_list[int(callback_query.data.split('_')[1])]]
        await bot.send_message(callback_query.from_user.id, text=
        f"Вы выбрали {date} {time_dict[time_list[int(callback_query.data.split('_')[1])]]}")
        return
    elif callback_query.data.split('_')[2] == "back":
        next_message_number = message_number - 1
    else:
        next_message_number = message_number + 1

    if len(time_dict) > next_message_number >= 0:
        choose_time = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("◀️", callback_data=f'choose_{next_message_number}_back'),
             InlineKeyboardButton("▶️", callback_data=f'choose_{next_message_number}_next')],
            [InlineKeyboardButton("Выбрать", callback_data=f'choose_{next_message_number}_choose')]
        ])
        text = time_list[next_message_number]
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=text,
            reply_markup=choose_time,
            parse_mode=ParseMode.HTML,
        )
    else:
        await bot.answer_callback_query(callback_query.id, "Это последнее запись.")




