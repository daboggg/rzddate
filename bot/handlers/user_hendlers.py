import logging
from datetime import date, timedelta, datetime

from aiogram import types, Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from babel.dates import format_date

from bot.keyboards.user_keyboards import get_years_kb, get_month_kb, get_day_kb, get_period_kb, confirm_kb
from utils.dbconnect import add_task
from utils.months import months

router = Router()
logger = logging.getLogger('bot.user_handlers')


class CalcDate(StatesGroup):
    start_calculation = State()
    year_selected = State()
    month_selected = State()
    day_selected = State()
    confirm = State()


@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message, state: FSMContext):
    reply_text1 = 'Привет, это бот для определения даты покупки билетов за 45, 60 или 90 дней.'
    reply_text2 = 'Выбери год'

    await message.answer(text=reply_text1)
    await message.answer(text=reply_text2, reply_markup=get_years_kb())
    await state.set_state(CalcDate.start_calculation)


@router.message()
async def msg_err(message: types.Message):
    await message.answer('пользуйтесь меню')


@router.callback_query(F.data == 'back', )
async def back(call: CallbackQuery, state: FSMContext):
    previous_state = ''
    current_state = str(await state.get_state())
    await call.message.answer('Возвращаемся на предыдущий шаг...')
    if 'year_selected' in current_state:
        previous_state = CalcDate.start_calculation
        await cmd_start(call.message, state)
    elif 'month_selected' in current_state:
        previous_state = CalcDate.year_selected
        await cb_year(call, state)
    elif 'day_selected' in current_state:
        previous_state = CalcDate.month_selected
        await cb_month(call, state)
    elif 'period_selected' in current_state:
        previous_state = CalcDate.day_selected
        await cb_day(call, state)

    await call.answer()
    await state.set_state(previous_state)


@router.callback_query(CalcDate.start_calculation)
async def cb_year(call: CallbackQuery, state: FSMContext):
    if call.data != 'back': await state.update_data(year=call.data)
    state_data = await state.get_data()
    reply_text = f'Выбран год: {state_data["year"]}\n'
    reply_text += 'Выбери месяц'
    logger.info(f'Выбран год: {state_data.get("year")}')
    await call.message.answer(text=reply_text, reply_markup=get_month_kb())
    await call.answer()
    await state.set_state(CalcDate.year_selected)


@router.callback_query(CalcDate.year_selected)
async def cb_month(call: CallbackQuery, state: FSMContext):
    if call.data != 'back': await state.update_data(month=call.data)
    state_data = await state.get_data()
    reply_text = f'Выбран год: {state_data["year"]}\n'
    reply_text += f'Выбран месяц: {months[int(state_data["month"]) - 1]}\n'
    reply_text += 'Выбери день'
    logger.info(f'Выбран месяц: {state_data.get("month")}')
    await call.message.answer(text=reply_text, reply_markup=get_day_kb(state_data))
    await call.answer()
    await state.set_state(CalcDate.month_selected)


@router.callback_query(CalcDate.month_selected)
async def cb_day(call: CallbackQuery, state: FSMContext):
    if call.data != 'back': await state.update_data(day=call.data)
    state_data = await state.get_data()
    reply_text = f'Выбран год: {state_data["year"]}\n'
    reply_text += f'Выбран месяц: {months[int(state_data["month"]) - 1]}\n'
    reply_text += f'Выбран день: {state_data["day"]}\n'
    reply_text += 'Выбери период'
    logger.info(f'Выбран день: {state_data.get("day")}')
    await call.message.answer(text=reply_text, reply_markup=get_period_kb())
    await call.answer()
    await state.set_state(CalcDate.day_selected)


@router.callback_query(CalcDate.day_selected)
async def cb_period(call: CallbackQuery, state: FSMContext):
    await state.update_data(period=call.data)
    state_data = await state.get_data()

    d = date(int(state_data['year']), int(state_data['month']), int(state_data['day']))
    date_of_purchase = d - timedelta(days=int(state_data['period']) - 1)
    await state.update_data(date_of_purchase=date_of_purchase)
    date_of_purchase_str = format_date(date_of_purchase, locale='ru', format='dd MMMM YYYY')
    d = format_date(d, locale='ru', format='dd MMMM YYYY')
    reply_text = f'Продажа на {d} открывается {date_of_purchase_str} ' \
                 f'(за {state_data["period"]} дней)'

    logger.info(f'Выбран период: {state_data.get("period")}')
    await call.message.answer(text=reply_text)

    # если вычисленная дата больше чем текущая, предложение о напоминании не выводим
    if date.today() < date_of_purchase:
        await call.message.answer("Хотите чтобы я напомнил?", reply_markup=confirm_kb())
        await state.set_state(CalcDate.confirm)
    else:
        await state.clear()
    await call.answer()


# установка или отмена напоминания
@router.callback_query(CalcDate.confirm)
async def cb_confirm(call: CallbackQuery, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    state_data = await state.get_data()
    dop = state_data['date_of_purchase']
    if call.data == 'confirm':

        id = f'date:{call.from_user.id}:{datetime.now().timestamp()}'
        trigg_name = 'date'
        chat_id = call.from_user.id
        run_date = str(date(dop.year, dop.month, dop.day))
        date_of_trip = str(date(int(state_data['year']), int(state_data['month']), int(state_data['day'])))

        await add_task(id,trigg_name,chat_id,run_date, date_of_trip)

        apscheduler.add_job(send_reminder, trigger=trigg_name,
                            id=id,
                            run_date=datetime(
                                dop.year,
                                dop.month,
                                dop.day,
                                7,
                                50,
                                0
                            ),
                            kwargs={'bot': bot, 'chat_id': chat_id,
                                    'text': f'Вы просили напомнить о покупке билета на {date_of_trip}'})
        logger.info(f'Задание добавлено в шедулер с id: {id}')
        await call.message.answer(f'Вы получите напоминание: {dop}, в 07:50')

    else:
        await call.message.answer('Чтобы начать сначала, нажмите /start в меню')
    await call.answer()
    await state.clear()


async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    await bot.send_message(chat_id, text)
