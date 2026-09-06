import asyncio
from aiogram import Dispatcher, Bot
from config import BOT_TOKEN
from handler import router
from database import init_db

async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())