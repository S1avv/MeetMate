from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.filters.callback_data import CallbackData

class Pagination(CallbackData, prefix="pag"):
    action: str

main = InlineKeyboardBuilder()
main.add(types.InlineKeyboardButton(
        text="👤 Профиль", 
        callback_data=Pagination(action="profile").pack())
    )

main.add(types.InlineKeyboardButton(
        text="🔎 Искать", 
        callback_data=Pagination(action="search").pack())
    )




profile = InlineKeyboardBuilder()

profile.add(types.InlineKeyboardButton(
        text="⛏️ Сменить отображаемое имя", 
        callback_data=Pagination(action="chang_name").pack())
    )

profile.add(types.InlineKeyboardButton(
        text="🎨 Фотография профиля", 
        callback_data=Pagination(action="chang_picture_menu").pack())
    )

profile.add(types.InlineKeyboardButton(
        text="⚙️ Сменить описание", 
        callback_data=Pagination(action="chang_descr").pack())
    )

profile.add(types.InlineKeyboardButton(
        text="🎩 Сменить пол", 
        callback_data=Pagination(action="gender").pack())
    )

profile.add(types.InlineKeyboardButton(
        text="🌏 Сменить страну", 
        callback_data=Pagination(action="chang_coun").pack())
    )

profile.add(types.InlineKeyboardButton(
        text="👤 Сменить возраст", 
        callback_data=Pagination(action="chang_age").pack())
    )

profile.add(types.InlineKeyboardButton(
        text="🧑‍🎓 Сменить хобби и интересы", 
        callback_data=Pagination(action="chang_hobby").pack())
    )

profile.add(types.InlineKeyboardButton(
        text="↩️ Назад", 
        callback_data=Pagination(action="main").pack())
    )

profile.adjust(1)




change_gender = InlineKeyboardBuilder()

change_gender.add(types.InlineKeyboardButton(
        text="🧑 Мужской", 
        callback_data=Pagination(action="gender_M").pack())
    )

change_gender.add(types.InlineKeyboardButton(
        text="👧 Женский", 
        callback_data=Pagination(action="gender_G").pack())
    )

change_gender.add(types.InlineKeyboardButton(
        text="↩️ Назад", 
        callback_data=Pagination(action="profile").pack())
    )

change_gender.adjust(1)




pic_change = InlineKeyboardBuilder()

pic_change.add(types.InlineKeyboardButton(
        text="➖ Удалить фото профиля", 
        callback_data=Pagination(action="pic_delete").pack())
    )

pic_change.add(types.InlineKeyboardButton(
        text="➕ Установить фото профиля", 
        callback_data=Pagination(action="chang_picture").pack())
    )

pic_change.add(types.InlineKeyboardButton(
        text="↩️ Назад", 
        callback_data=Pagination(action="profile").pack())
    )

pic_change.adjust(1)


error = InlineKeyboardBuilder()

error.add(types.InlineKeyboardButton(
        text="↩️ Назад", 
        callback_data=Pagination(action="profile").pack())
    )