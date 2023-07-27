from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

general_inf = KeyboardButton('Записаться')
my_notes = KeyboardButton('Мои записи')
number = KeyboardButton("Номер", request_contact=True)

menu_main = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, selective=True
).add(general_inf).add(my_notes).add(number)
