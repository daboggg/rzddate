import logging
from datetime import datetime, timedelta

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.user_hendlers import send_reminder
from utils.dbconnect import get_tasks, delete_task

logger = logging.getLogger('utils.recovery')

# добаляет задание в шедулер из бд при старте приложения
async def add_tasks_to_scheduler(scheduler: AsyncIOScheduler, bot: Bot) -> None:
    tasks_list = await get_tasks()

    if len(tasks_list):
        for task in tasks_list:
            rd = datetime.strptime(task[3], "%Y-%m-%d")
            #  если текущее время меньше времени запуска, добавить задание в шедулер
            if datetime.now() < rd:
                text = f'\n\nваш текст: <b>{task[5]}</b>'
                scheduler.add_job(send_reminder,
                                  trigger=task[1],
                                  id=task[0],
                                  run_date=datetime(rd.year, rd.month, rd.day, 7, 50, 0),
                                  # run_date=datetime.now()+ timedelta(minutes=1),
                                  kwargs={'bot': bot,
                                          'chat_id': task[2],
                                          'text': f'Вы просили напомнить о покупке билета на {task[4]}{text}'
                                          }
                                  )
                logger.info(f'Задание добавлено в шедулер с id: {task[0]}')
            # иначе удалить задание из бд
            else:
                delete_task(task[0])
