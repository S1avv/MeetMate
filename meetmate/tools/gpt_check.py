import pytgpt.phind as phind
import asyncio

async def request_gpt(text):
    bot = phind.PHIND()

    response = bot.chat(text)

    return response