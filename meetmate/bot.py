from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message

from config import bot
from handlers.start import start_cmd
from handlers.message_type import messages_type

import asyncio


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(start_cmd)
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
