from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_tg.loader import dp, bot
from buttons.inlines import connect
from buttons.reply import number
from states import UserStates
from calendar_api.individual_calendar import IndividualCalendar
from calendar_api.group_calendar import GroupCalendar
from calendar_api.thematic_calendar import ThematicCalendar


@dp.message_handler(state=UserStates.GetNumber)
async def get_name_number(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await bot.send_message(message.chat.id, text="И остался последний шаг, поделитесь своим номером телефона, "
                                                 "чтобы психолог смог с вами связаться, для этого "
                                                 "нажмите на кнопку ниже",
                           reply_markup=number
                           )

    await UserStates.ReqestCont.set()


@dp.message_handler(content_types=['contact'], state=UserStates.ReqestCont)
async def my_number(message: Message, state: FSMContext):

    async with state.proxy() as data:
        event = data["event"]
        cons = data["cons"]
        try:
            subgroup = data["subgroup"]
        except:
            subgroup = None

    if cons == "ind_cons":
        cons = "Индивидуальная консультация"
    elif cons == "mini_group":
        cons = "Мини-группа"
    elif cons == "them_group":
        if subgroup == "about_relat":
            subgroup = "Про отношения"
        elif subgroup == "self_realization":
            subgroup = "Самореализация"
        elif subgroup == "finance":
            subgroup = "Финансы"
        cons = "Тематические группы"

    async with state.proxy() as data:
        text = data.get("text")
    event_data = {
        "summary": cons,
        "subgroup": subgroup,
        "name": text,
        "phone_number": message.contact["phone_number"],
        "start": f"{event['date']['year']}-{event['date']['month']}-{event['date']['day']}T{event['startTime']}+03:00",
        "end": f"{event['date']['year']}-{event['date']['month']}-{event['date']['day']}T{event['endTime']}+03:00",
    }
    if cons == "Индивидуальная консультация":
        event_id = IndividualCalendar.edit_event(event_data["start"], event_data["end"], event_data)
    elif cons == "Мини-группа":
        event_id = GroupCalendar.edit_event(event_data["start"], event_data["end"], event_data)
    elif cons == "Тематические группы":
        event_id = ThematicCalendar.edit_event(event_data["start"], event_data["end"], event_data)
    event_data["event_id"] = event_id

    text = f"""
Вы записались на этот слот:

<b>Название:</b> {event_data['summary']} 😊
<b>Дата:</b> {event['date']['day']}.{event['date']['month']}.{event['date']['year']} 📅
<b>Время начала встречи:</b> {event['startTime'][:-3]} ⏰
<b>Конец встречи:</b> {event['endTime'][:-3]} 🕒
<b>Ваше имя:</b> {text}
<b>Ваш номер телефона:</b> {message.contact["phone_number"]}
    """
    await bot.send_message(message.chat.id, text=text, parse_mode=types.ParseMode.HTML, reply_markup=connect)
    await state.finish()
