#!/usr/bin/env python3
import os
import logging
from tronpy import Tron
from tronpy.providers import HTTPProvider

logger = logging.getLogger(__name__)

def create_tron_client():
    api_key = os.getenv("TRONGRID_API_KEY")

    if api_key:
        logger.info("🔐 Используется TRONGRID API ключ для подключения к TronGrid.")
        return Tron(HTTPProvider(api_key=api_key))
    else:
        logger.warning("⚠️ TRONGRID_API_KEY не найден. Используется подключение по умолчанию.")
        return Tron()
