import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from session import SESSIONS
from states import BotStates

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🔐 Завершить сессию")
async def logout(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    session_existed = uid in SESSIONS
    SESSIONS.pop(uid, None)

    await state.clear()

    if session_existed:
        logger.info(f"🔐 Пользователь {uid} завершил сессию")
        await msg.answer("🔐 Сессия завершена. Приватный ключ удалён.", reply_markup=ReplyKeyboardRemove())
    else:
        logger.warning(f"⚠️ Попытка завершить несуществующую сессию от user_id={uid}")
        await msg.answer("❗ У вас нет активной сессии.")
