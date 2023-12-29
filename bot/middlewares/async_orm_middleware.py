from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db.orm import AsyncORM


class AsyncOrmMiddleware(BaseMiddleware):
    def __init__(self, async_orm: AsyncORM):
        self.async_orm = async_orm

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['async_orm'] = self.async_orm
        return await handler(event,data)