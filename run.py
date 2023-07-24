from aiogram.utils import executor


if __name__ == "__main__":
    from bot_tg.loader import dp

    executor.start_polling(dp, skip_updates=True)