from aiogram import types

from bot_tg.loader import dp, bot
from buttons.inlines import week_button_markup, this_weeks_button_markup, next_weeks_button_markup, cd, subgroup_them

cons = None
subgroup = None


@dp.callback_query_handler(cd.filter(action="ind_cons"))
async def ind_cons_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Индивидуальная консультация-это встреча с психологом (Гештальт-терапевтом), на которой ты сможешь поделиться '
        'тем, что тебя беспокоит или тем, что ты хочешь изменить.\n\n'
        'Также задашь свои вопросы и узнаешь себя лучше.\n\n'
        'ℹ️Работа по изменению структуры личности требует регулярных встреч.\n\n'
        'ℹ️Короткий ситуационный запрос подразумевает от 4 до 8 консультаций.\n\n'
        'Бережно. Конфиденциально.\n\n'
        'Приходи , я рада тебе 🤍'
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Запись ведется на следующую неделю. Выберете подходящий день и время 🕙",
        reply_markup=week_button_markup
    )
    global cons
    cons = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='mini_group'))
async def mini_cons_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Мини-группа предназначена для глубокой и активной работы по заданной теме.\n\n"
        "В группе принимают участие до 4 человек.\n\n"
        "Присоединиться к ближайшей группе по актуальной для тебя теме можно здесь 🔽🔽🔽",
        reply_markup=week_button_markup
    )
    global cons
    cons = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='them_group'))
async def them_cons_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Групповые семинары и мастер -классы предназначены для проработки конкретных тем, актуальных"
        " для всех участников.\n\n"
        "Выбирай интересную тему , приходи и расширяй свои возможности , осознанность и формируй свой собственный "
        "поддерживающий круг единомышленников 🙌",
        reply_markup=subgroup_them
    )
    global cons
    cons = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='about_relat'))
async def subgroup_relat_them_callback(callback_query: types.CallbackQuery):
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
        reply_markup=week_button_markup
    )
    global subgroup
    subgroup = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='self_realization'))
async def subgroup_realization_them_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Самореализация\n\n'
        'Курс «В ритме собственной души». Работа в закрытой группе с возможность индивидуальной обратной связи. '
        'Будем исследовать свои сильные слабые стороны, свою собственную «магию» жизни, талантов, призвания и '
        'скоростей. Встречи каждые 3 недели. Online',
        reply_markup=week_button_markup
    )
    global subgroup
    subgroup = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='finance'))
async def subgroup_realization_them_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Курс Pro финансы .\n\n'
        'Динамическая группа для тех, кто хочет раскачать свое финансовое поле. Встречи 1 раз в месяц, закрытая группа '
        'с собственной траекторией ближайшего развития. 6 встреч = 6 месяцев. Online.',
        reply_markup=week_button_markup
    )
    global subgroup
    subgroup = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='this_week'))
async def this_week_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Выберите в какой день хотите провести встречу',
        reply_markup=this_weeks_button_markup
    )


@dp.callback_query_handler(cd.filter(action='next_week'))
async def next_week_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Выберите в какой день хотите провести встречу',
        reply_markup=next_weeks_button_markup
    )


@dp.callback_query_handler(lambda c: c.data.startswith('date_'))
async def date_callback_function(callback_query: types.CallbackQuery):
    if callback_query.data.split('_')[1] == "back":
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        return
    selected_date = callback_query.data.split('_')[1]
    if cons == "ind_cons":
        conf = "индивидуальной"
    elif cons == "mini_group":
        conf = "мини групп"
    else:
        conf = "Тематической"
    if subgroup:
        print(subgroup)
    await bot.answer_callback_query(callback_query.id, text=f"Вы выбрали день {selected_date} для {conf} встречи!")
