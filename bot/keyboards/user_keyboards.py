from datetime import date
from typing import Any

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.months import months


def get_years_kb() -> InlineKeyboardMarkup:
    """Get years kb
    """
    current_year = date.today().year
    ikm = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=str(current_year), callback_data=str(current_year)),
            InlineKeyboardButton(text=str(current_year + 1), callback_data=str(current_year + 1)),
        ]
    ], resize_keyboard=True)

    return ikm


def get_month_kb() -> InlineKeyboardMarkup:
    ikm = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=months[m - 1], callback_data=str(m)) for m in range(1, 5)],
        [InlineKeyboardButton(text=months[m - 1], callback_data=str(m)) for m in range(5, 9)],
        [InlineKeyboardButton(text=months[m - 1], callback_data=str(m)) for m in range(9, 13)],
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ], resize_keyboard=True)
    return ikm


def get_day_kb(state_data) -> InlineKeyboardMarkup:
    year = int(state_data['year'])
    month = int(state_data['month'])

    daysInMonth = 0
    if month == 2: daysInMonth = 29 if year % 4 == 0 else 28
    if month in [1, 3, 5, 7, 8, 10, 12]: daysInMonth = 31
    if month in [4, 6, 9, 11]: daysInMonth = 30

    ikm = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(m), callback_data=str(m)) for m in range(1, 8)],
        [InlineKeyboardButton(text=str(m), callback_data=str(m)) for m in range(8, 15)],
        [InlineKeyboardButton(text=str(m), callback_data=str(m)) for m in range(15, 22)],
        [InlineKeyboardButton(text=str(m), callback_data=str(m)) for m in range(22, 29)],
        [InlineKeyboardButton(text=str(m), callback_data=str(m)) for m in range(29, daysInMonth + 1)],
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ], resize_keyboard=True)
    return ikm


def get_period_kb() -> InlineKeyboardMarkup:
    ikm = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='45', callback_data='45'),
            InlineKeyboardButton(text='60', callback_data='60'),
            InlineKeyboardButton(text='90', callback_data='90'),
        ],
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ], resize_keyboard=True)
    return ikm


def confirm_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.button(text='Да', callback_data='confirm')
    ikb.button(text='Нет', callback_data='cancel')
    return ikb.adjust(2).as_markup()


def delete_task_kb(info: list[dict[str,Any]]) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for i in info:
        date_to_button = str(i['date'])
        text_to_butoon = i['text']
        text_to_butoon = text_to_butoon[text_to_butoon.find('<b>')+3:-4]

        ikb.button(text=f'{date_to_button} {text_to_butoon}', callback_data=f'deletetask_{i["job_id"]}')
    return ikb.adjust(1).as_markup()
