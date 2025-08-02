#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logger.debug("📦 Загрузка переменных окружения из .env...")
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRONGRID_API_KEY = os.getenv("TRONGRID_API_KEY")

if BOT_TOKEN:
    logger.debug("✅ BOT_TOKEN загружен.")
else:
    logger.warning("⚠️ BOT_TOKEN не найден в переменных окружения!")

if TRONGRID_API_KEY:
    logger.debug("✅ TRONGRID_API_KEY загружен.")
else:
    logger.warning("⚠️ TRONGRID_API_KEY не найден в переменных окружения!")
