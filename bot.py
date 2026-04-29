import asyncio
from aiogram import Dispatcher, Bot
from config import BOT_TOKEN
from handler import router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())