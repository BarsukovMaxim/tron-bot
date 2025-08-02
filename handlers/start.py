import logging
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from html import escape
from tronpy.keys import PrivateKey
from tron.client import create_tron_client
from keyboards import KEYBOARD
from session import SESSIONS
from datetime import datetime, timedelta, timezone

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    logger.info(f"👋 Пользователь {msg.from_user.id} отправил /start")
    await msg.answer(
        "Привет! Введи команду `/auth <PRIVATE_KEY>` для авторизации.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("auth"))
async def cmd_auth(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    args = msg.text.strip().split()

    if len(args) != 2:
        logger.warning(f"⚠️ Неверный формат команды /auth от user_id={uid}")
        return await msg.answer("Формат: `/auth <PRIVATE_KEY>`")

    private_key = args[1]
    if len(private_key) != 64:
        logger.warning(f"⛔ Приватный ключ некорректной длины от user_id={uid}")
        return await msg.answer("❌ Приватный ключ должен быть длиной 64 символа (hex)")

    try:
        pk = PrivateKey(bytes.fromhex(private_key))
        client = create_tron_client()
        address = pk.public_key.to_base58check_address()

        SESSIONS[uid] = {
            "pk": pk,
            "client": client,
            "address": address,
            "expires": datetime.now(timezone.utc) + timedelta(minutes=10)
        }

        await state.clear()
        logger.info(f"✅ Успешная авторизация user_id={uid}, address={address}")
        await msg.answer(
            f"✅ Авторизация прошла успешно!\n"
            f"Ваш адрес: `{address}`\n"
            f"Сессия будет активна 10 минут.",
            reply_markup=KEYBOARD
        )

    except Exception as e:
        logger.exception(f"❌ Ошибка авторизации user_id={uid}")
        await msg.answer(f"❌ Ошибка авторизации:\n`{escape(str(e))}`")
        await state.clear()
