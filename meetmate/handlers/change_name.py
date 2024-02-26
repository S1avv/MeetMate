from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

import aiosqlite

from keyboards import builder

chang_nameuser = Router()


@chang_nameuser.callback_query(builder.Pagination.filter(F.action == "chang_name"))
async def main_starter(callback_query: types.CallbackQuery) -> None:
    photo_path = "meetmate/assets/start.png"

    media = InputMediaPhoto(media=FSInputFile(photo_path), caption="✏️ Введите новое имя пользователя (макс. 16 символов)")

    await callback_query.message.edit_media(media=media)

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        async with db.execute("UPDATE users SET input_type = ?, callback_query = ? WHERE id = ?",
                              ("name", str(callback_query.message.message_id), callback_query.from_user.id)) as cursor:
            await db.commit()