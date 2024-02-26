from aiogram.filters import Command, CommandObject, CommandStart
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

from tools.account_manager import verify_account
from tools.gpt_check import request_gpt
from handlers.profile import get_completed_profile
from keyboards import builder
from config import bot, TOKEN

import asyncio
import os
import aiosqlite
import requests

import os
from PIL import Image
import io


photo_ty = Router()


URI_INFO = f"http://api.telegram.org/bot{TOKEN}/getFile?file_id="
URI = f"http://api.telegram.org/file/bot{TOKEN}/"


@photo_ty.message(F.photo)
async def messages_cmd(message: Message):
    await verify_account(message)

    file_id = message.photo[3].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()["result"]["file_path"]
    img = requests.get(URI+img_path)

    img = Image.open(io.BytesIO(img.content))

    photo_path = f"meetmate/avatars/{message.from_user.id}.png"

    if os.path.exists(photo_path):
        os.remove(photo_path)

    img.save(f"meetmate/avatars/{message.from_user.id}.png")

    await message.delete()

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM profiles WHERE id = {message.from_user.id}")
        profiles_data = await cursor.fetchone()

        await cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}")
        users_data = await cursor.fetchone()

        await cursor.execute("UPDATE users SET input_type = ? WHERE id = ?", ("None", str(message.from_user.id)))

        await db.commit()

        caption = (
            f"🚀 Профиль пользователя {message.from_user.username}\n\n"
            f"• Имя: <b>{profiles_data[1]}</b>\n\n"
            f"• Описание: <b>{profiles_data[2]}</b>\n\n"
            f"• Пол: <b>{profiles_data[4]}</b>\n\n"
            f"• Страна: <b>{profiles_data[5]}</b>\n\n"
            f"• Возраст: <b>{profiles_data[6]}</b>\n\n"
            f"• Немного о хобби и интересах: <b>{profiles_data[7]}</b>\n\n"
            f"📂 Фото профиля: <b>{"Есть" if os.path.exists(os.path.join("avatars", str({message.from_user.id}))) else "Нету"}</b>"
        )

        file_path = os.path.join(f"meetmate/avatars", f"{message.from_user.id}.png")

        photo_path = f"meetmate/avatars/{message.from_user.id}.png"

        if os.path.exists(photo_path):
            pass
        else:
            photo_path = "meetmate/assets/start.png"
            
        media = InputMediaPhoto(media=FSInputFile(photo_path), caption=caption)

        await bot.edit_message_media(media=media, chat_id=message.from_user.id, message_id=users_data[5], reply_markup=builder.profile.as_markup())