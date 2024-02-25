from aiogram.filters import Command, CommandObject, CommandStart
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

from tools.account_manager import verify_account
from tools.gpt_check import request_gpt
from handlers.profile import get_completed_profile
from keyboards import builder
from config import bot

import asyncio
import os
import aiosqlite

messages_type = Router()

@messages_type.message()
async def messages_cmd(message: Message):
    await verify_account(message)

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}")
        users_data = await cursor.fetchone()

        await cursor.execute(f"SELECT * FROM profiles WHERE id = {message.from_user.id}")
        profile_data = await cursor.fetchone()

        if users_data[4] == 'description':
            verify = await request_gpt(f"Verify the text for the presence of offensive language: '{message.text}' If there is offensive language in this text, write True; if not, then False. Always provide the response in one word.")

            if "True" in verify:
                await message.delete()
                sent_message = await message.answer("❌ К сожалению, обнаружена нецензурная лексика в вашем сообщении. Пожалуйста, обратите внимание на тон вашего выражения")
                
                await asyncio.sleep(4)
                
                await sent_message.delete()
                return 
            
            await cursor.execute("UPDATE profiles SET description = ? WHERE id = ?", (message.text, str(message.from_user.id)))
            await cursor.execute("UPDATE users SET input_type = ? WHERE id = ?", ("None", str(message.from_user.id)))

            caption = (
                f"🚀 Профиль пользователя {message.from_user.username}\n\n"
                f"• Имя: <b>{profile_data[1]}</b>\n\n"
                f"• Описание: <b>{message.text}</b>\n\n"
                f"• Пол: <b>{profile_data[4]}</b>\n\n"
                f"• Страна: <b>{profile_data[5]}</b>\n\n"
                f"• Возраст: <b>{profile_data[6]}</b>\n\n"
                f"• Немного о хобби и интересах: <b>{profile_data[7]}</b>\n\n"
                f"📂 Фото профиля: <b>{"Есть" if os.path.exists(os.path.join("avatars", str({message.from_user.id}))) else "Нету"}</b>"
            )

            photo_path = f"meetmate/avatars/{message.from_user.id}.png" if os.path.join(f"meetmate/avatars", f"{message.from_user.id}.png") else "meetmate/assets/start.png"

            media = InputMediaPhoto(media=FSInputFile(photo_path), caption=caption)

            await bot.edit_message_media(media=media, chat_id=message.from_user.id, message_id=users_data[5], reply_markup=builder.profile.as_markup())

            await db.commit()

            await message.delete()

        elif users_data[4] == 'country':
            verify = await request_gpt(f"Here's the text sent by the user: '{message.text}', extract the country from this text and provide a one-word response in the following format: 'Flag emoji of the Country'. If there is no country in the text, simply output 'False'. Make sure to output in this format: 'Flag of the country you found, and then the country itself")

            if "False" in verify:
                await message.delete()

                sent_message = await message.answer("❌ Произошла непредвиденная ошибка. Введите название страны еще раз, пожалуйста.")

                await asyncio.sleep(4)
                
                await sent_message.delete()
                return 
            

            await cursor.execute("UPDATE profiles SET country = ? WHERE id = ?", (verify, str(message.from_user.id)))
            await cursor.execute("UPDATE users SET input_type = ? WHERE id = ?", ("None", str(message.from_user.id)))

            await db.commit()

            caption = (
                f"🚀 Профиль пользователя {message.from_user.username}\n\n"
                f"• Имя: <b>{profile_data[1]}</b>\n\n"
                f"• Описание: <b>{profile_data[2]}</b>\n\n"
                f"• Пол: <b>{profile_data[4]}</b>\n\n"
                f"• Страна: <b>{verify}</b>\n\n"
                f"• Возраст: <b>{profile_data[6]}</b>\n\n"
                f"• Немного о хобби и интересах: <b>{profile_data[7]}</b>\n\n"
                f"📂 Фото профиля: <b>{"Есть" if os.path.exists(os.path.join("avatars", str({message.from_user.id}))) else "Нету"}</b>"
            )

            photo_path = f"meetmate/avatars/{message.from_user.id}.png" if os.path.join(f"meetmate/avatars", f"{message.from_user.id}.png") else "meetmate/assets/start.png"

            media = InputMediaPhoto(media=FSInputFile(photo_path), caption=caption)

            await bot.edit_message_media(media=media, chat_id=message.from_user.id, message_id=users_data[5], reply_markup=builder.profile.as_markup())


            await message.delete()
        else:
            await message.delete()