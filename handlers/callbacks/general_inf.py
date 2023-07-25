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
        'Рассказываем про индивидуальные консультации\n'
        'Выберите на какой неделе хотите провести встречу на этой или следующей',
        reply_markup=week_button_markup
    )
    global cons
    cons = cd.parse(callback_query.data)["action"]

@dp.callback_query_handler(cd.filter(action='mini_group'))
async def mini_cons_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Рассказываем про мини группы\n'
        'Выберите на какой неделе хотите провести встречу на этой или следующей',
        reply_markup=week_button_markup
    )
    global cons
    cons = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='them_group'))
async def them_cons_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Рассказываем про тематические группы\n'
        'Выберите на какой неделе хотите провести встречу на этой или следующей',
        reply_markup=subgroup_them
    )
    global cons
    cons = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='about_relat'))
async def subgroup_relat_them_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Рассказываем про отношения',
        reply_markup=week_button_markup
    )
    global subgroup
    subgroup = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='self_realization'))
async def subgroup_realization_them_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Рассказываем про самореализацию',
        reply_markup=week_button_markup
    )
    global subgroup
    subgroup = cd.parse(callback_query.data)["action"]


@dp.callback_query_handler(cd.filter(action='finance'))
async def subgroup_realization_them_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        'Рассказываем про финансы',
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