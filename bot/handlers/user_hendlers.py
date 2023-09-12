from datetime import date, timedelta

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from babel.dates import format_date

from bot.keyboards.user_keyboards import get_years_kb, get_month_kb, get_day_kb, get_period_kb
from utils.months import months

router = Router()


class CalcDate(StatesGroup):
    start_calculation = State()
    year_selected = State()
    month_selected = State()
    day_selected = State()


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


@router.callback_query(F.data =='back', )
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
    await call.message.answer(text=reply_text, reply_markup=get_month_kb())
    await call.answer()
    await state.set_state(CalcDate.year_selected)


@router.callback_query(CalcDate.year_selected)
async def cb_month(call: CallbackQuery, state: FSMContext):
    if call.data != 'back': await state.update_data(month=call.data)
    state_data = await state.get_data()
    reply_text = f'Выбран год: {state_data["year"]}\n'
    reply_text += f'Выбран месяц: {months[int(state_data["month"])-1]}\n'
    reply_text += 'Выбери день'
    await call.message.answer(text=reply_text, reply_markup=get_day_kb(state_data))
    await call.answer()
    await state.set_state(CalcDate.month_selected)


@router.callback_query(CalcDate.month_selected)
async def cb_day(call: CallbackQuery, state: FSMContext):
    if call.data != 'back': await state.update_data(day=call.data)
    state_data = await state.get_data()
    reply_text = f'Выбран год: {state_data["year"]}\n'
    reply_text += f'Выбран месяц: {months[int(state_data["month"])-1]}\n'
    reply_text += f'Выбран день: {state_data["day"]}\n'
    reply_text += 'Выбери период'
    await call.message.answer(text=reply_text, reply_markup=get_period_kb())
    await call.answer()
    await state.set_state(CalcDate.day_selected)


@router.callback_query(CalcDate.day_selected)
async def cb_period(call: CallbackQuery, state: FSMContext):
    await state.update_data(period=call.data)
    state_data = await state.get_data()

    d = date(int(state_data['year']), int(state_data['month']), int(state_data['day']))
    date_of_purchase = d - timedelta(days=int(state_data['period']) - 1)
    date_of_purchase = format_date(date_of_purchase, locale='ru', format='dd MMMM YYYY')
    d = format_date(d, locale='ru', format='dd MMMM YYYY')
    reply_text = f'Продажа на {d} открывается {date_of_purchase} (за {state_data["period"]} дней)'

    await call.message.answer(text=reply_text)
    await call.answer()
    await state.clear()
