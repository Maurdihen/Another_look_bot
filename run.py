from handlers import dp
from aiogram.contrib.middlewares.logging import LoggingMiddleware

dp.middleware.setup(LoggingMiddleware())


if __name__ == "__main__":
    from aiogram.utils import executor

    executor.start_polling(dp, skip_updates=True)
