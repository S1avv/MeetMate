from aiogram.filters import Command, CommandObject, CommandStart
from aiogram import Router, types, F
from aiogram.types import Message

from tools.account_manager import verify_account

import asyncio
import sqlite3

messages_type = Router()

@messages_type.message()
async def messages_cmd(message: Message):
    await verify_account(message)

    with sqlite3.connect("meetmate/database.sqlite") as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}")
        result = cursor.fetchone()

    if result[4] == 'description':
        await message.answer("Данные успешно записаны!")
    else:
        await message.delete()

    