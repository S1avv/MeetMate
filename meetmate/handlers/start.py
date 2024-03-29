from aiogram.filters import Command, CommandObject, CommandStart
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.types import FSInputFile

from tools.account_manager import verify_account
from keyboards import builder

import asyncio

start_cmd = Router()


@start_cmd.message(CommandStart())
async def start_c(message: Message):
    await verify_account(message)

    photo_path = "meetmate/assets/start.png"
    
    await message.reply_photo(photo=FSInputFile(photo_path), caption=(
        "👋 Привет!\n\n"
        "Рады видеть тебя здесь в нашем боте!\n\n"
        "• Здесь вы можете листать профили других пользователей и выражать своё восхищение, ставя лайки тем, кто вам нравится.\n\n"
        "Удачи в поиске и приятного времяпрепровождения! 💖✨"
    ), reply_markup=builder.main.as_markup())
