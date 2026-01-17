import asyncio  
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import logging
from logging_config import setup_logging

from config import TELEGRAM_BOT_TOKEN

setup_logging()

logger = logging.getLogger(__name__)
logger.info("Bot is starting...")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        "Hello world!"
    )

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())