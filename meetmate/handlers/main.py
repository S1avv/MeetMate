from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile

from keyboards import builder

main_router = Router()

@main_router.callback_query(builder.Pagination.filter(F.action == "main"))
async def main_starter(callback_query: types.CallbackQuery) -> None:
    caption=(
        "👋 Привет!\n\n"
        "Рады видеть тебя здесь в нашем боте!\n\n"
        "• Здесь вы можете листать профили других пользователей и выражать своё восхищение, ставя лайки тем, кто вам нравится.\n\n"
        "Удачи в поиске и приятного времяпрепровождения! 💖✨"
    )

    photo_path = "meetmate/assets/start.png"

    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=caption)

    await callback_query.message.edit_media(media=media, reply_markup=builder.main.as_markup())