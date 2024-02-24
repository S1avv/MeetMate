from aiogram.filters import Command, CommandObject, CommandStart
from aiogram import Router, types, F
from aiogram.types import Message

from tools.account_manager import verify_account

import asyncio

start_cmd = Router()


@start_cmd.message(CommandStart())
async def start_c(message: Message):
    await verify_account(message)

    await message.reply((
        "👋 Привет!\n\n"
        "Рады видеть тебя здесь в нашем боте!\n\n"
        "• Здесь вы можете листать профили других пользователей и выражать своё восхищение, ставя лайки тем, кто вам нравится.\n\n"
        "Удачи в поиске и приятного времяпрепровождения! 💖✨"
    ))