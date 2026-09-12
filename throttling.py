from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache
import asyncio


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 2.0):
        self.rate_limit = rate_limit
        self.cache = TTLCache(maxsize=10_000, ttl=self.rate_limit)
    async def __call__(self,handler,event,data):
        user_id = event.from_user.id
        if user_id in self.cache:
            await event.answer("Не спамь, слишком быстро")
            return

        self.cache[user_id] = True
        return await handler(event, data)