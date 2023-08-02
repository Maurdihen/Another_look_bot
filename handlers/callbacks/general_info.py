from aiogram import types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from bot_tg.loader import dp, bot
from buttons.inlines import this_weeks_button_markup, cd, subgroup_them, enroll, next_
from calendar_api.individual_calendar import Calendar
from utils import convert_date
from states import UserStates

from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(cd.filter(action="ind_cons"), state=UserStates.ChooseCat)
async def ind_cons_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Индивидуальная консультация-это встреча с психологом (Гештальт-терапевтом), на которой ты сможешь поделиться '
        'тем, что тебя беспокоит или тем, что ты хочешь изменить.\n\n'
        'Также задашь свои вопросы и узнаешь себя лучше.\n\n'
        'ℹ️Работа по изменению структуры личности требует регулярных встреч.\n\n'
        'ℹ️Короткий ситуационный запрос подразумевает от 4 до 8 консультаций.\n\n'
        'Бережно. Конфиденциально.\n\n'
        'Приходи , я рада тебе 🤍',
        reply_markup=enroll
    )

    async with state.proxy() as data:
        data["cons"] = cd.parse(callback_query.data)["action"]

    await UserStates.Enroll.set()


@dp.callback_query_handler(cd.filter(action="enroll"), state=UserStates.Enroll)
async def enroll_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Запись ведется на следующую неделю. Выберете подходящий день и время 🕙',
        reply_markup=this_weeks_button_markup
    )

    await UserStates.ChooseDay.set()


@dp.callback_query_handler(cd.filter(action='mini_group'), state=UserStates.ChooseCat)
async def mini_cons_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Мини-группа предназначена для глубокой и активной работы по заданной теме.\n\n"
        "В группе принимают участие до 4 человек.\n\n"
        "Присоединиться к ближайшей группе по актуальной для тебя теме можно здесь 🔽🔽🔽",
        reply_markup=enroll
    )

    async with state.proxy() as data:
        data["cons"] = cd.parse(callback_query.data)["action"]

    await UserStates.Enroll.set()


@dp.callback_query_handler(cd.filter(action='them_group'), state=UserStates.ChooseCat)
async def them_cons_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Групповые семинары и мастер -классы предназначены для проработки конкретных тем, актуальных"
        " для всех участников.\n\n"
        "Выбирай интересную тему , приходи и расширяй свои возможности , осознанность и формируй свой собственный "
        "поддерживающий круг единомышленников 🙌",
        reply_markup=subgroup_them
    )

    async with state.proxy() as data:
        data["cons"] = cd.parse(callback_query.data)["action"]

    await UserStates.Subgroup.set()


@dp.callback_query_handler(cd.filter(action='about_relat'), state=UserStates.Subgroup)
async def subgroup_relat_them_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Курс «Про отношения»\n\n'
        'Теория , практические упражнения.\n'
        '- Личные границы\n'
        '- Типы привязанности и их взаимодействие\n'
        '- Созависимость и контрзависимость\n'
        '- Этапы развития романтических отношений \n'
        '- Блищость духовная и физическая\n'
        'Мужской и женский взгляд 👀 комфортная скорость для привнесения теории в жизнь. Online',
        reply_markup=enroll
    )
    async with state.proxy() as data:
        data["subgroup"] = cd.parse(callback_query.data)["action"]

    await UserStates.Enroll.set()


@dp.callback_query_handler(cd.filter(action='self_realization'), state=UserStates.Subgroup)
async def subgroup_realization_them_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Самореализация\n\n'
        'Курс «В ритме собственной души». Работа в закрытой группе с возможность индивидуальной обратной связи. '
        'Будем исследовать свои сильные слабые стороны, свою собственную «магию» жизни, талантов, призвания и '
        'скоростей. Встречи каждые 3 недели. Online',
        reply_markup=enroll
    )
    async with state.proxy() as data:
        data["subgroup"] = cd.parse(callback_query.data)["action"]

    await UserStates.Enroll.set()


@dp.callback_query_handler(cd.filter(action='finance'), state=UserStates.Subgroup)
async def subgroup_realization_them_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Курс Pro финансы .\n\n'
        'Динамическая группа для тех, кто хочет раскачать свое финансовое поле. Встречи 1 раз в месяц, закрытая группа '
        'с собственной траекторией ближайшего развития. 6 встреч = 6 месяцев. Online.',
        reply_markup=enroll
    )

    async with state.proxy() as data:
        data["subgroup"] = cd.parse(callback_query.data)["action"]

    await UserStates.Enroll.set()


@dp.callback_query_handler(lambda c: c.data.startswith('date_'), state=UserStates.ChooseDay)
async def date_callback_function(callback_query: types.CallbackQuery, state: FSMContext):
    selected_date = callback_query.data.split('_')[1]
    date = convert_date(selected_date) + "+03:00"

    async with state.proxy() as data:
        cons = data["cons"]
        try:
            subgroup = data["subgroup"]
        except:
            pass


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
        cons = f"Тематические группы {subgroup}"

    print(cons, date)
    events = Calendar.check_calendar(date, cons)
    print(events)
    async with state.proxy() as data:
        data["events"] = events

    if len(events) == 0:
        await bot.send_message(callback_query.from_user.id, text="Сори в этот день нет свободных слотов")
        return

    await bot.send_message(callback_query.from_user.id, text="Вы можете записаться в такие слоты:")
    await bot.send_message(callback_query.from_user.id, text=events[0], reply_markup=next_)

    await UserStates.ChooseTime.set()


@dp.callback_query_handler(lambda c: c.data.startswith('next_'), state=UserStates.ChooseTime)
async def next_callback(callback_query: types.CallbackQuery, state: FSMContext):
    message_number = int(callback_query.data.split('_')[1])

    async with state.proxy() as data:
        events = data["events"]

    if callback_query.data.split('_')[2] == "signup":
        await bot.send_message(callback_query.from_user.id, text="Для того чтобы бот смог вас записать отправте "
                                                                 "пожалуйста своё имя и фамилию в формате Имя Фамилия")

        event = events[int(callback_query.data.split('_')[1])]
        print(events[int(callback_query.data.split('_')[1])])

        async with state.proxy() as data:
            data["event"] = event

        await UserStates.GetNumber.set()
        return
    elif callback_query.data.split('_')[2] == "back":
        next_message_number = message_number - 1
    else:
        next_message_number = message_number + 1

    if len(events) > next_message_number >= 0:
        next_ = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Далее", callback_data=f'next_{next_message_number}_next')],
            [InlineKeyboardButton("Записаться", callback_data=f'next_{next_message_number}_signup')],
            [InlineKeyboardButton("Назад", callback_data=f'next_{next_message_number}_back')],
        ])

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=[next_message_number],
            reply_markup=next_,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await bot.answer_callback_query(callback_query.id, "Это последнее запись.")


@dp.callback_query_handler(lambda c: c.data.startswith('back'), state="*")
async def back_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    async with state.proxy() as data:
        cons = data["cons"]
    if cons == "them_group":
        if await state.get_state() == "UserStates:Subgroup":
            await UserStates.ChooseCat.set()
        elif await state.get_state() == "UserStates:Enroll":
            await UserStates.Subgroup.set()
        elif await state.get_state() == "UserStates:ChooseDay":
            await UserStates.Enroll.set()
    else:
        if await state.get_state() == "UserStates:ChooseDay":
            await UserStates.Enroll.set()
        else:
            await UserStates.previous()
