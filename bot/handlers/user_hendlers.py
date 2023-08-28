from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from datetime import date, timedelta
from babel.dates import format_date

from bot.keyboards.user_keyboards import get_start_kb, get_years_kb, get_month_kb, get_day_kb, get_period_kb
from utils import months


class CalcDate(StatesGroup):
    start_calculation = State()
    year_selected = State()
    month_selected = State()
    day_selected = State()


async def cmd_start(message: types.Message, state: FSMContext):
    reply_text1 = 'Привет, это бот для определения даты покупки билетов за 45, 60 или 90 дней.'
    reply_text2 = 'Выбери год'

    await message.answer(text=reply_text1, reply_markup=get_start_kb())
    await message.answer(text=reply_text2, reply_markup=get_years_kb())
    await state.set_state(CalcDate.start_calculation)


async def cb_year(call: CallbackQuery, state: FSMContext):
    if call.data != 'back': await state.update_data(year=call.data)
    state_data = await state.get_data()
    reply_text = f'Выбран год: {state_data["year"]}\n'
    reply_text += 'Выбери месяц'
    await call.message.answer(text=reply_text, reply_markup=get_month_kb())
    await call.answer()
    await state.set_state(CalcDate.year_selected)


async def cb_month(call: CallbackQuery, state: FSMContext):
    if call.data != 'back': await state.update_data(month=call.data)
    state_data = await state.get_data()
    reply_text = f'Выбран год: {state_data["year"]}\n'
    reply_text += f'Выбран месяц: {months[int(state_data["month"])-1]}\n'
    reply_text += 'Выбери день'
    await call.message.answer(text=reply_text, reply_markup=get_day_kb(state_data))
    await call.answer()
    await state.set_state(CalcDate.month_selected)


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
    await state.finish()


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


async def msg_err(message: types.Message, state: FSMContext):
    await message.answer('пользуйтесь кнопками')


async def anything(message: types.Message):
    await message.answer('Я тебя не понимаю...')


def register_handler(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(msg_err, state='*')
    dp.register_callback_query_handler(back, Text(equals='back'), state='*')
    dp.register_callback_query_handler(cb_year, state=CalcDate.start_calculation)
    dp.register_callback_query_handler(cb_month, state=CalcDate.year_selected)
    dp.register_callback_query_handler(cb_day, state=CalcDate.month_selected)
    dp.register_callback_query_handler(cb_period, state=CalcDate.day_selected)
    dp.register_message_handler(anything)
