import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cd = CallbackData("ikd", "action")


# General Info Keyboard Markup
general_info_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Индивидуальные консультации', callback_data=cd.new("ind_cons"))],
    [InlineKeyboardButton('Мини-группы', callback_data=cd.new("mini_group"))],
    [InlineKeyboardButton('Тематические группы', callback_data=cd.new("them_group"))]
])

general_info_markup_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Индивидуальные консультации', callback_data="admin_indCons")],
    [InlineKeyboardButton('Мини-группы', callback_data="admin_miniGroup")],
    [InlineKeyboardButton('Тематические группы', callback_data="admin_themGroup")]
])

# This Week's Keyboard Markup
today = datetime.date.today()
current_month = today.month

# Создание списка кнопок с датой или "-"
this_weeks_button_list = []
cnt = 0
day_of_week_short = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота"
}
while cnt <= 7:
    date = today + datetime.timedelta(days=cnt)
    day_num = date.weekday()

    # Пропускаем добавление кнопки для воскресенья (day_num == 6)
    if day_num != 6:
        this_weeks_button_list.append(InlineKeyboardButton(f"📆{day_of_week_short[day_num]} {date.strftime('%d.%m')}",
                                                           callback_data=f"date_{date.strftime('%d.%m.%Y')}"))
    cnt += 1

back_button = InlineKeyboardButton('⬅️ Назад', callback_data="back")
this_weeks_button_list.append(back_button)

this_weeks_button_markup = InlineKeyboardMarkup(row_width=1).add(*this_weeks_button_list)


subgroup_them = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Про отношения', callback_data=cd.new("about_relat"))],
    [InlineKeyboardButton('Самореализация', callback_data=cd.new("self_realization"))],
    [InlineKeyboardButton('Про финансы', callback_data=cd.new("finance"))],
    [InlineKeyboardButton('⬅️ Назад', callback_data="back")]
])



enroll = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Записаться', callback_data=cd.new("enroll"))],
    [InlineKeyboardButton('⬅️ Назад', callback_data="back")]
])

enroll_them_mini = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Записаться', callback_data=cd.new("enroll_them_mini"))],
    [InlineKeyboardButton('⬅️ Назад', callback_data="back")]
])

connect = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Связаться с психологом', url="https://t.me/Evgeniya_drugoy_vzglyad")]
])


next_ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("◀️", callback_data='next_0_back'), InlineKeyboardButton("▶️", callback_data='next_0_next')],
    [InlineKeyboardButton("Записаться", callback_data='next_0_signup')],
    [InlineKeyboardButton("⬅️ Назад", callback_data='back')]
])

choose_time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("◀️", callback_data='choose_0_back'), InlineKeyboardButton("▶️", callback_data='choose_0_next')],
    [InlineKeyboardButton("Выбрать", callback_data='choose_0_choose')]
])

create_look_slots = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Создать ивент", callback_data=cd.new('create_slots'))],
    [InlineKeyboardButton("Посмотреть инфу про встречи", callback_data=cd.new('look_slots'))]
])

free_occupied_slots = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Свободные слоты", callback_data=cd.new('free_slots'))],
    [InlineKeyboardButton("Занятые слоты", callback_data=cd.new('occupied_slots'))]
])