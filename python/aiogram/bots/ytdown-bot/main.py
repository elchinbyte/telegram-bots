import asyncio  
import logging
from logging_config import setup_logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from yt_down import download_audio, download_video, get_latest_file
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

@dp.message(F.text.contains("http"))
async def handle_url(message: Message):
    download_video(message.text)
    file_path = get_latest_file("video")
    
    if file_path:
        file_path = FSInputFile(file_path)
        await bot.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption="Here is your downloaded video",
            request_timeout=300
        )
    else:
        await message.answer("No video found.")

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())