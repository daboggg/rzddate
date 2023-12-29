import asyncio

from db.database import async_engine
from db.models import Base

class AsyncORM:

    async def create_table(self):
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

asyncio.run(AsyncORM().create_table())