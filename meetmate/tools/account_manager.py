from aiogram.filters import Command, CommandObject, CommandStart
from aiogram import Router, types, F
from aiogram.types import Message

import sqlite3
import asyncio
from datetime import datetime

async def verify_account(message):
    with sqlite3.connect("meetmate/database.sqlite") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
        result = cursor.fetchone()

        if result:
            return True
        else:
            cursor.execute(f"INSERT INTO users (id, username, first_name, creation_data, input_type) VALUES ('{message.from_user.id}', '{message.from_user.username}', '{message.from_user.first_name}', '{datetime.now().strftime("%d:%m:%Y - %H:%M")}', 'None')")
            cursor.execute(f"INSERT INTO profiles (id, name, description) VALUES ('{message.from_user.id}', 'None', 'None')")
            