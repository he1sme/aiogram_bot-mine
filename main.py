import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.database import async_main


async def main():
    await async_main()
    bot = Bot(token='7058220566:AAGi8fUZf2QHNG6MfOXvPC-dU-HMO_NpXWA')
    dp = Dispatcher()
    dp.include_router(router)
    print('BOT IS ACTIVATED')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
