import asyncio
import logging

from sqlalchemy import select

from db.database import async_engine, async_session_factory, session_factory
from db.models import Base, Task

logger = logging.getLogger('db.orm')


class AsyncORM:

    async def create_table(self) -> None:
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            logger.info(f'Таблица(ы) создана(ы)')

    async def add_task(self, task: Task) -> None:
        async with async_session_factory() as session:
            session.add(task)
            await session.commit()

    async def get_tasks(self) -> list[Task]:
        async with async_session_factory() as session:
            query = select(Task)
            result = await session.execute(query)
            tasks = result.scalars().all()
            logger.info(f'Получен список заданий из бд:\n {tasks=}')
            return tasks

    async def get_task(self, id: str) -> Task:
        async with async_session_factory() as session:
            stmt = select(Task).where(Task.id == id)
            res = await session.scalars(stmt)
            logger.info(f'Получено задание из бд с id={id}')
            return res.one()


class SyncORM:

    @staticmethod
    def delete_task(id: str) -> None:
        with session_factory() as session:
            task = session.get(Task, id)
            session.delete(task)
            session.commit()


asyncio.run(AsyncORM().create_table())
