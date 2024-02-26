from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

import aiosqlite

from keyboards import builder

chang_age_menu = Router()


@chang_age_menu.callback_query(builder.Pagination.filter(F.action == "chang_age"))
async def changed_age(callback_query: types.CallbackQuery) -> None:
    photo_path = "meetmate/assets/start.png"

    media = InputMediaPhoto(media=FSInputFile(photo_path), caption="👨‍💼 Введите свой возраст")

    await callback_query.message.edit_media(media=media)

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        async with db.execute("UPDATE users SET input_type = ?, callback_query = ? WHERE id = ?",
                              ("age", str(callback_query.message.message_id), callback_query.from_user.id)) as cursor:
            await db.commit()