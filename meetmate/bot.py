from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message

from config import bot
from handlers.start import start_cmd
from handlers.message_type import messages_type
from handlers.profile import profile_data
from handlers.main import main_router
from handlers.change_description import chang_descr
from handlers.change_country import chang_coun
from handlers.change_gender import chang_gend
from handlers.photo_type import photo_ty
from handlers.change_picture import chang_pic
from handlers.change_name import chang_nameuser
from handlers.change_age import chang_age_menu
from handlers.change_hobby import chang_hobby_menu

import asyncio


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(start_cmd)
    dp.include_router(photo_ty)
    dp.include_router(chang_hobby_menu)
    dp.include_router(chang_age_menu)
    dp.include_router(chang_nameuser)
    dp.include_router(chang_coun)
    dp.include_router(chang_gend)
    dp.include_router(chang_pic)
    dp.include_router(chang_descr)
    dp.include_router(main_router)
    dp.include_router(profile_data)
    dp.include_router(messages_type)



async def main() -> None:
    print("Bot started!")

    dp = Dispatcher()

    register_routers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has been stopped")