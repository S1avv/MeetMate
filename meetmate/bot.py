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

import asyncio


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(start_cmd)
    dp.include_router(chang_coun)
    dp.include_router(chang_gend)
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