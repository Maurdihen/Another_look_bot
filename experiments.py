from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = '5978072325:AAGJL5l2a04ceKw7rSRtwUK8E8DkGNNH1Ek'  # Замените на свой API-токен, полученный от BotFather

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    contact_button = types.KeyboardButton(text="Поделиться контактом", request_contact=True)
    keyboard.add(contact_button)
    await message.reply("Привет! Нажми на кнопку, чтобы поделиться контактом.", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'share_contact')
async def process_callback_share_contact(callback_query: types.CallbackQuery):
    keyboard = types.ReplyKeyboardRemove()  # Скрыть клавиатуру после нажатия кнопки

    # Получим контактные данные пользователя из объекта callback_query
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    last_name = callback_query.from_user.last_name

    # Проверяем, есть ли у пользователя контактные данные
    if callback_query.from_user.contact is not None:
        contact = callback_query.from_user.contact
        phone_number = contact.phone_number
        # Отправляем контактные данные обратно пользователю
        await bot.send_contact(user_id, phone_number=phone_number, first_name=first_name, last_name=last_name,
                               reply_markup=keyboard)
    else:
        await bot.send_message(user_id, "У вас нет сохраненного контакта. Пожалуйста, предоставьте его в настройках "
                                        "Telegram и повторите попытку.", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
