import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.keyboards.user_keyboards import delete_task_kb

delete_handlers_router = Router()
logger = logging.getLogger('bot.user_handlers')


# отправляет клавиатуру для удаления заданий
@delete_handlers_router.message(Command(commands=['delete']))
async def offer_delete_task(message: Message, apscheduler: AsyncIOScheduler) -> None:
    f = filter(lambda j: j.id.split(":")[0] == str(message.from_user.id), apscheduler.get_jobs())
    m = map(lambda j: {
        'job_id': j.id,
        'date': j.trigger.run_date.date(),
        'text': j.kwargs['text']
    }, f)
    info = list(m)
    if len(info):
        await message.answer('👇 Нажмите для удаления', reply_markup=delete_task_kb(info))
    else:
        await message.answer('⛔ Напоминаний нет')


# удаляет задания
@delete_handlers_router.callback_query(F.data.startswith("deletetask_"))
async def delete_task(callback: CallbackQuery, apscheduler: AsyncIOScheduler) -> None:
    apscheduler.remove_job(callback.data.split("_")[1])
    logger.info(f'задание с id {callback.data.split("_")[1]} удалено из шедулера')
    await callback.message.answer('❌ Удалено')
    await callback.answer()
