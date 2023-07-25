import calendar
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '5978072325:AAGJL5l2a04ceKw7rSRtwUK8E8DkGNNH1Ek'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    inline_markup = create_date_inline_keyboard()

    await message.reply("Привет! Давай выберем день для встречи.", reply_markup=inline_markup)


@dp.callback_query_handler(lambda c: c.data == 'back')
async def process_date_selection(callback_query: types.CallbackQuery):
    selected_date = callback_query.data.split('_')[1]
    await bot.answer_callback_query(callback_query.id, text=f"Вы выбрали день {selected_date} для встречи!1")

def create_date_inline_keyboard():
    inline_markup = types.InlineKeyboardMarkup(row_width=7)

    today = datetime.date.today()
    current_month = today.month

    for i in range(7):
        date = today + datetime.timedelta(days=i)
        date_str = date.strftime("%d.%m.%Y")
        callback_data = f"date_{date_str}"
        emoji = "🗓️" if date.month == current_month else " "
        inline_markup.insert(types.InlineKeyboardButton(f"{emoji} {date.strftime('%d')}", callback_data=callback_data))

    next_week = today + datetime.timedelta(weeks=1)
    callback_data_next_week = f"date_next_{next_week.strftime('%d.%m.%Y')}"
    inline_markup.insert(types.InlineKeyboardButton("➡️ Назад", callback_data=callback_data_next_week))

    return inline_markup


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)