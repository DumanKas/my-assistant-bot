import asyncio
from aiogram import Dispatcher, Bot, BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Any, Dict
from handler import router
from database import init_db, create_pool
from config import BOT_TOKEN
class PoolMiddleware(BaseMiddleware):
    def __init__(self, pool):
        self.pool = pool
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],event: TelegramObject,data: Dict[str, Any]) -> Any:
        data["pool"] = self.pool
        return await handler(event, data)

async def main():
    pool = await create_pool()
    await init_db(pool)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.message.middleware(PoolMiddleware(pool))
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())