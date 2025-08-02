#!/usr/bin/env python3
import logging
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

logger = logging.getLogger(__name__)
logger.debug("🔧 Создание пользовательской клавиатуры...")

KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📤 Делегировать")],
        [KeyboardButton(text="📊 Баланс"), KeyboardButton(text="🔐 Завершить сессию")]
    ],
    resize_keyboard=True
)

CONFIRM_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_delegate"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_delegate"),
        ]
    ]
)

logger.debug("✅ Клавиатура создана.")
