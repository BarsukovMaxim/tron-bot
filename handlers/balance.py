import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from html import escape
from session import SESSIONS
from states import BotStates

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📊 Баланс")
async def balance(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    session = SESSIONS.get(uid)
    if not session:
        logger.warning(f"⛔ Попытка получить баланс без сессии от пользователя {uid}")
        return await msg.answer("Сначала авторизуйтесь через `/auth <PRIVATE_KEY>`")

    try:
        client = session["client"]
        address = session["address"]

        balance = client.get_account_balance(address)
        res = client.get_account_resource(address)

        energy_total = res.get('EnergyLimit', 0)
        energy_used = res.get('EnergyUsed', 0)
        bw_total = res.get('freeNetLimit', 0)
        bw_used = res.get('freeNetUsed', 0)

        logger.info(f"📊 Пользователь {uid} запросил баланс {address}: {balance} TRX")

        await msg.answer(
            f"💰 Адрес: `{address}`\n"
            f"TRX: {balance}\n"
            f"⚡ Energy: {energy_total - energy_used} / {energy_total}\n"
            f"📶 Bandwidth: {bw_total - bw_used} / {bw_total}"
        )
        await state.clear()
    except Exception as e:
        logger.exception(f"❌ Ошибка при получении баланса для пользователя {uid}")
        await msg.answer(f"❌ Ошибка получения баланса:\n`{escape(str(e))}`")
        await state.clear()
