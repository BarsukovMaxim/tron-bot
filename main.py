#!/usr/bin/env python3
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from logging_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

from config import BOT_TOKEN
from handlers import register_handlers
from session import cleanup_sessions


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

async def main():
    logger.info("🚀 Бот запускается")
    register_handlers(dp)
    asyncio.create_task(cleanup_sessions())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())