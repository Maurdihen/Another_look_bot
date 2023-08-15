from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio

API_TOKEN = '5978072325:AAGJL5l2a04ceKw7rSRtwUK8E8DkGNNH1Ek'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text_message(message: types.Message):
    await message.reply(f"Вы отправили текстовое сообщение: {message.text}")


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def handle_contact(message: types.Message):
    contact = message.contact
    await message.reply(f"Вы отправили контакт:\nИмя: {contact.first_name}\nНомер телефона: {contact.phone_number}")


if __name__ == '__main__':
    from aiogram import executor
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)
