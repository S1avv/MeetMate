from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

from keyboards import builder

import aiosqlite
import os

profile_data = Router()

@profile_data.callback_query(builder.Pagination.filter(F.action == "profile"))
async def get_completed_profile(callback_query: types.CallbackQuery) -> None:
    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM profiles WHERE id = {callback_query.from_user.id}")
        users_data = await cursor.fetchone()

        async with db.execute("UPDATE users SET input_type = ?, callback_query = ? WHERE id = ?",
                              ("None", str(callback_query.message.message_id), callback_query.from_user.id)) as cursor:
            await db.commit()

        file_path = os.path.join(f"meetmate/avatars", f"{callback_query.from_user.id}.png")

        photo_path = f"meetmate/avatars/{callback_query.from_user.id}.png"
        if os.path.exists(photo_path):
            pass
        else:
            photo_path = "meetmate/assets/start.png"

        new_caption = (
            f"🚀 Профиль пользователя {callback_query.from_user.username}\n\n"
            f"• Имя: <b>{users_data[1]}</b>\n\n"
            f"• Описание: <b>{users_data[2]}</b>\n\n"
            f"• Пол: <b>{users_data[4]}</b>\n\n"
            f"• Страна: <b>{users_data[5]}</b>\n\n"
            f"• Возраст: <b>{users_data[6]}</b>\n\n"
            f"• Немного о хобби и интересах: <b>{users_data[7]}</b>\n\n"
            f"📂 Фото профиля: <b>{'Есть' if os.path.exists(file_path) else 'Нету'}</b>"
        )

        media = InputMediaPhoto(media=FSInputFile(photo_path), caption=new_caption)

        await callback_query.message.edit_media(media=media, reply_markup=builder.profile.as_markup())