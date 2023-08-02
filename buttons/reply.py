from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

general_inf = KeyboardButton('Записаться')
my_notes = KeyboardButton('Мои записи')

menu_main = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, selective=True
).add(general_inf).add(my_notes)

number = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, selective=True
).add(KeyboardButton("Поделиться номером", request_contact=True)).add(KeyboardButton("Ввести номер в ручную"))
