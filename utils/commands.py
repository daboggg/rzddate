from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начать вычисление даты'
        ),
        BotCommand(
            command='delete',
            description='Удалить напоминание'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
