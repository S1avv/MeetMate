from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

import aiosqlite

from keyboards import builder

chang_hobby_menu = Router()


@chang_hobby_menu.callback_query(builder.Pagination.filter(F.action == "chang_hobby"))
async def changed_age(callback_query: types.CallbackQuery) -> None:
    photo_path = "meetmate/assets/start.png"

    media = InputMediaPhoto(media=FSInputFile(photo_path), caption="🚀 Напиши о своих хобби (макс. 80 символов)")

    await callback_query.message.edit_media(media=media)

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        async with db.execute("UPDATE users SET input_type = ?, callback_query = ? WHERE id = ?",
                              ("hobby", str(callback_query.message.message_id), callback_query.from_user.id)) as cursor:
            await db.commit()