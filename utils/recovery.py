import logging
from datetime import datetime, timedelta

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.user_hendlers import send_reminder
from db.models import Task
from db.orm import AsyncORM, SyncORM

logger = logging.getLogger('utils.recovery')

# добаляет задание в шедулер из бд при старте приложения
async def add_tasks_to_scheduler(scheduler: AsyncIOScheduler, bot: Bot, async_orm: AsyncORM) -> None:
    tasks_list: list['Task'] = await async_orm.get_tasks()

    if len(tasks_list):
        for task in tasks_list:
            rd = datetime.strptime(task.run_date, "%Y-%m-%d")
            #  если текущее время меньше времени запуска, добавить задание в шедулер
            if datetime.now() < rd:
                text = f'\n\nваш текст: <b>{task.text}</b>'
                scheduler.add_job(send_reminder,
                                  trigger=task.trigg_name,
                                  id=task.id,
                                  run_date=datetime(rd.year, rd.month, rd.day, 7, 50, 0),
                                  # run_date=datetime.now()+ timedelta(minutes=1),
                                  kwargs={'bot': bot,
                                          'chat_id': task.chat_id,
                                          'text': f'⚠️ Вы просили напомнить о покупке билета на {task.date_of_trip}{text}'
                                          }
                                  )
                logger.info(f'Задание добавлено в шедулер с id: {task.id}')
            # иначе удалить задание из бд
            else:
                SyncORM.delete_task(task.id)
