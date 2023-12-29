import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler import events

from bot.handlers.delete_handlers import delete_handlers_router
from bot.handlers.user_hendlers import user_handlers_router
from bot.middlewares.apschedmiddleware import SchedulerMiddleware
from bot.middlewares.async_orm_middleware import AsyncOrmMiddleware
from db.orm import AsyncORM
from settings import settings
from utils.commands import set_commands
from utils.delete_task_from_db import delete_task_from_db
from utils.recovery import add_tasks_to_scheduler


async def start_bot(bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

                        )
    logger = logging.getLogger('main')

    # создаю при старте бд
    async_orm = AsyncORM()


    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()

    # слушаю событие EVENT_JOB_REMOVED и удаляю задание из бд
    scheduler.add_listener(delete_task_from_db, events.EVENT_JOB_REMOVED)

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    # добавляю задания в шедулер из бд (если есть)
    await add_tasks_to_scheduler(scheduler, bot)

    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    # регистрация middlewares
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.update.middleware.register(AsyncOrmMiddleware(async_orm))

    # подключение роутеров
    dp.include_routers(
        delete_handlers_router,
        user_handlers_router,

    )
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    logger.info('start')

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())

