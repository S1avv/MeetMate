from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

import aiosqlite
import os

from keyboards import builder

chang_pic = Router()


@chang_pic.callback_query(builder.Pagination.filter(F.action == "chang_picture"))
async def main_starter(callback_query: types.CallbackQuery) -> None:

    photo_path = f"meetmate/avatars/{callback_query.from_user.id}.png"

    if os.path.exists(photo_path):
        media = InputMediaPhoto(media=FSInputFile(photo_path), caption="🖼️ Ваша текущая фотография профиля:\n\n• Чтобы изменить фотографию, отправьте новую.\n\nМинимальный размер 1150x1150 пикселей")

        await callback_query.message.edit_media(media=media)
    else:
        photo_path = "meetmate/assets/start.png"

        media = InputMediaPhoto(media=FSInputFile(photo_path), caption="🖼️ Вы еще не установили фотографию профиля\n\n• Чтобы установить фотографию, отправьте ее мне.\n\nМинимальный размер 1150x1150 пикселей")

        await callback_query.message.edit_media(media=media)

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        async with db.execute("UPDATE users SET input_type = ?, callback_query = ? WHERE id = ?",
                              ("picture", str(callback_query.message.message_id), callback_query.from_user.id)) as cursor:
            await db.commit()


@chang_pic.callback_query(builder.Pagination.filter(F.action == "pic_delete"))
async def chang_pics(callback_query: types.CallbackQuery) -> None:

    photo_path = f"meetmate/avatars/{callback_query.from_user.id}.png"

    if os.path.exists(photo_path):
        os.remove(photo_path)

        media = InputMediaPhoto(media=FSInputFile("meetmate/assets/start.png"), caption="✅ Удаление успешно завершено!")

        await callback_query.message.edit_media(media=media, reply_markup=builder.error.as_markup())
    else:
        await callback_query.message.edit_caption(caption="🚫 Ошибка! Ваш профиль не содержит фотографии. \n\nПожалуйста, добавьте фотографию профиля.", reply_markup=builder.error.as_markup())



@chang_pic.callback_query(builder.Pagination.filter(F.action == "chang_picture_menu"))
async def chang_pics(callback_query: types.CallbackQuery) -> None:

    await callback_query.message.edit_caption(caption="🎨 Выберите действие: ", reply_markup=builder.pic_change.as_markup())