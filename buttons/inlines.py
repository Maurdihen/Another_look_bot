import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils import get_start_end_of_week

cd = CallbackData("ikd", "action")


# General Info Keyboard Markup
general_info_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Индивидуальные консультации', callback_data=cd.new("ind_cons"))],
    [InlineKeyboardButton('Мини-группы', callback_data=cd.new("mini_group"))],
    [InlineKeyboardButton('Тематические группы', callback_data=cd.new("them_group"))]
])

# Week Selection Keyboard Markup
week_button_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(f'На этой неделе ({get_start_end_of_week()})', callback_data=cd.new('this_week'))],
    [InlineKeyboardButton(f'На следующей неделе ({get_start_end_of_week(next_week=True)})', callback_data=cd.new('next_week'))]
])

# This Week's Keyboard Markup
today = datetime.date.today()
current_month = today.month

# Создание списка кнопок с датой или "-"
this_weeks_button_list = []
cnt = 0
day_of_week_short = {
    0: "Пн",
    1: "Вт",
    2: "Ср",
    3: "Чт",
    4: "Пт",
    5: "Сб"
}
for i in range(7):
    date = today + datetime.timedelta(days=cnt)
    if date.weekday() != 6:
        day_num = date.weekday()
        this_weeks_button_list.append(InlineKeyboardButton(f"🗓️{day_of_week_short[day_num]}-{date.strftime('%d')}",
                                                                callback_data=f"date_{date.strftime('%d.%m.%Y')}"))
        cnt += 1
    else:
        cnt += 1
        date = today + datetime.timedelta(days=cnt)
        day_num = date.weekday()
        this_weeks_button_list.append(InlineKeyboardButton(f"🗓️{day_of_week_short[day_num]}-{date.strftime('%d')}",
                                                           callback_data=f"date_{date.strftime('%d.%m.%Y')}"))
        cnt += 1

back_button = InlineKeyboardButton("⬅️ Назад", callback_data="date_back")
this_weeks_button_list.append(back_button)

this_weeks_button_markup = InlineKeyboardMarkup(row_width=7).add(*this_weeks_button_list)

# Next Week's Keyboard Markup
# next_week_today = today + datetime.timedelta(days=7)
# next_current_month = next_week_today.month
# next_weeks_button_list = [
#     InlineKeyboardButton(f"🗓️ {next_date.strftime('%d')}",
#                          callback_data=f"date_{next_date.strftime('%d.%m.%Y')}")
#     for next_date in [next_week_today + datetime.timedelta(days=i) for i in range(7)]
# ]
#
# back_button = InlineKeyboardButton("⬅️ Назад", callback_data="date_back")
# next_weeks_button_list.append(back_button)
#
# next_weeks_button_markup = InlineKeyboardMarkup(row_width=7).add(*next_weeks_button_list)


subgroup_them = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Про отношения', callback_data=cd.new("about_relat")),
     InlineKeyboardButton('Самореализация', callback_data=cd.new("self_realization")),
     InlineKeyboardButton('Про финансы', callback_data=cd.new("finance"))],
    [InlineKeyboardButton('⬅️ Назад', callback_data="date_back")]
])



enroll = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Записаться', callback_data=cd.new("enroll"))],
    [InlineKeyboardButton('⬅️ Назад', callback_data="date_back")]
])
