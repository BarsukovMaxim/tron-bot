import logging
from aiogram import Dispatcher

from . import start, balance, delegate, logout

logger = logging.getLogger(__name__)


def register_handlers(dp: Dispatcher):
    logger.info("📦 Регистрируются хендлеры...")
    dp.include_router(start.router)
    dp.include_router(balance.router)
    dp.include_router(delegate.router)
    dp.include_router(logout.router)
    logger.info("✅ Хендлеры зарегистрированы")
