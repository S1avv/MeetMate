from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

import aiosqlite

from keyboards import builder
from config import bot

import os

chang_gend = Router()


@chang_gend.callback_query(builder.Pagination.filter(F.action == "gender"))
async def main_starter(callback_query: types.CallbackQuery) -> None:

    photo_path = "meetmate/assets/start.png"

    media = InputMediaPhoto(media=FSInputFile(photo_path), caption="👤 Выберите пол")

    await callback_query.message.edit_media(media=media, reply_markup=builder.change_gender.as_markup())

    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        async with db.execute("UPDATE users SET input_type = ?, callback_query = ? WHERE id = ?",
                              ("gender", str(callback_query.message.message_id), callback_query.from_user.id)) as cursor:
            await db.commit()

@chang_gend.callback_query(builder.Pagination.filter(F.action == "gender_M"))
async def gen_m(callback_query: types.CallbackQuery) -> None:
    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM profiles WHERE id = {callback_query.from_user.id}")
        profiles_data = await cursor.fetchone()

        await cursor.execute(f"SELECT * FROM users WHERE id = {callback_query.from_user.id}")
        users_data = await cursor.fetchone()

        await cursor.execute("UPDATE profiles SET gender = ? WHERE id = ?", ("M", str(callback_query.from_user.id)))

        await db.commit()

        caption = (
            f"🚀 Профиль пользователя {callback_query.from_user.username}\n\n"
            f"• Имя: <b>{profiles_data[1]}</b>\n\n"
            f"• Описание: <b>{profiles_data[2]}</b>\n\n"
            f"• Пол: <b>M</b>\n\n"
            f"• Страна: <b>{profiles_data[5]}</b>\n\n"
            f"• Возраст: <b>{profiles_data[6]}</b>\n\n"
            f"• Немного о хобби и интересах: <b>{profiles_data[7]}</b>\n\n"
            f"📂 Фото профиля: <b>{"Есть" if os.path.exists(os.path.join("avatars", str({callback_query.from_user.id}))) else "Нету"}</b>"
        )

        file_path = os.path.join(f"meetmate/avatars", f"{callback_query.from_user.id}.png")

        photo_path = f"meetmate/avatars/{callback_query.from_user.id}.png"
        if os.path.exists(photo_path):
            pass
        else:
            photo_path = "meetmate/assets/start.png"

        media = InputMediaPhoto(media=FSInputFile(photo_path), caption=caption)

        await bot.edit_message_media(media=media, chat_id=callback_query.from_user.id, message_id=users_data[5], reply_markup=builder.profile.as_markup())


@chang_gend.callback_query(builder.Pagination.filter(F.action == "gender_G"))
async def gen_g(callback_query: types.CallbackQuery) -> None:
    async with aiosqlite.connect("meetmate/database.sqlite") as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM profiles WHERE id = {callback_query.from_user.id}")
        profiles_data = await cursor.fetchone()

        await cursor.execute(f"SELECT * FROM users WHERE id = {callback_query.from_user.id}")
        users_data = await cursor.fetchone()

        await cursor.execute("UPDATE profiles SET gender = ? WHERE id = ?", ("Д", str(callback_query.from_user.id)))

        await db.commit()

        caption = (
            f"🚀 Профиль пользователя {callback_query.from_user.username}\n\n"
            f"• Имя: <b>{profiles_data[1]}</b>\n\n"
            f"• Описание: <b>{profiles_data[2]}</b>\n\n"
            f"• Пол: <b>Д</b>\n\n"
            f"• Страна: <b>{profiles_data[5]}</b>\n\n"
            f"• Возраст: <b>{profiles_data[6]}</b>\n\n"
            f"• Немного о хобби и интересах: <b>{profiles_data[7]}</b>\n\n"
            f"📂 Фото профиля: <b>{"Есть" if os.path.exists(os.path.join("avatars", str({callback_query.from_user.id}))) else "Нету"}</b>"
        )

        file_path = os.path.join(f"meetmate/avatars", f"{callback_query.from_user.id}.png")

        photo_path = f"meetmate/avatars/{callback_query.from_user.id}.png"
        if os.path.exists(photo_path):
            pass
        else:
            photo_path = "meetmate/assets/start.png"
        media = InputMediaPhoto(media=FSInputFile(photo_path), caption=caption)

        await bot.edit_message_media(media=media, chat_id=callback_query.from_user.id, message_id=users_data[5], reply_markup=builder.profile.as_markup())