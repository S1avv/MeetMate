from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

import aiosqlite

from keyboards import builder

chang_coun = Router()


@chang_coun.callback_query(builder.Pagination.filter(F.action == "chang_coun"))
async def main_starter(callback_query: types.CallbackQuery) -> None:
    photo_path = "meetmate/assets/start.png"

    media = InputMediaPhoto(media=FSInputFile(photo_path), caption="🌏 Введите страну в который вы проживаете")

    await callback_query.message.edit_media(media=media)

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        async with db.execute("UPDATE users SET input_type = ?, callback_query = ? WHERE id = ?",
                              ("country", str(callback_query.message.message_id), callback_query.from_user.id)) as cursor:
            await db.commit()