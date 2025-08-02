import logging
from html import escape
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import BotStates
from keyboards import CONFIRM_INLINE_KEYBOARD
from session import SESSIONS

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "📤 Делегировать")
async def delegate_start(msg: Message, state: FSMContext):
    uid = msg.from_user.id

    if uid not in SESSIONS:
        logger.warning(f"⛔ Попытка делегирования без авторизации: user_id={uid}")
        return await msg.answer("Сначала авторизуйтесь через `/auth <PRIVATE_KEY>`")

    await state.set_state(BotStates.waiting_for_delegate_input)
    logger.info(f"🟡 Ожидание адреса и суммы ENERGY от user_id={uid}")
    await msg.answer(
        "Отправьте адрес и количество ENERGY, которое хотите делегировать.\n"
        "Пример: `Txxxxx 300`"
    )


@router.message(BotStates.waiting_for_delegate_input)
async def handle_delegate_input(msg: Message, state: FSMContext):
    uid = msg.from_user.id

    session = SESSIONS.get(uid)
    if not session:
        logger.warning(f"⛔ Попытка делегирования без сессии user_id={uid}")
        await msg.answer("Сначала авторизуйтесь через /auth <PRIVATE_KEY>")
        return await state.clear()

    try:
        to_address, energy_str = msg.text.strip().split()
        energy = int(float(energy_str))
        trx_amount = int(energy / 10.08)  # Коэффициент из TronLink

        await state.update_data(
            to_address=to_address,
            energy=energy,
            trx_amount=trx_amount,
        )
        await state.set_state(BotStates.waiting_for_delegate_confirm)

        await msg.answer(
            f"⚠️ Подтвердите делегирование ENERGY:\n"
            f"🔸 Адрес: `{to_address}`\n"
            f"🔸 ENERGY: {energy}\n",
            reply_markup=CONFIRM_INLINE_KEYBOARD
        )

    except Exception as e:
        logger.warning(f"❌ Ошибка парсинга параметров ENERGY user_id={uid}: {e}")
        await msg.answer("⚠️ Формат: `Txxxxx 300` — адрес и количество ENERGY.")
        await state.clear()


@router.callback_query(F.data.in_(["confirm_delegate", "cancel_delegate"]))
async def handle_delegate_confirm(cb: CallbackQuery, state: FSMContext):
    uid = cb.from_user.id
    data = await state.get_data()

    if cb.data == "cancel_delegate":
        await cb.message.edit_text("❌ Делегирование отменено пользователем.")
        logger.info(f"🚫 Делегирование отменено user_id={uid}")
        return await state.clear()

    session = SESSIONS.get(uid)
    if not session:
        logger.warning(f"⛔ Подтверждение без сессии user_id={uid}")
        await cb.message.edit_text("Сначала авторизуйтесь через /auth <PRIVATE_KEY>")
        return await state.clear()

    try:
        client = session["client"]
        pk = session["pk"]
        from_address = session["address"]

        tx = (
            client.trx.delegate_resource(
                owner=from_address,
                receiver=data["to_address"],
                balance=int(data["trx_amount"] * 1_000_000),
                resource="ENERGY",
                lock=False,
            )
            .fee_limit(5_000_000)
            .build()
        )

        result = tx.sign(pk).broadcast()
        txid = result.get("txid", "N/A")

        logger.info(f"✅ Делегировано {data['energy']} ENERGY от {from_address} на {data['to_address']} (TX: {txid})")

        await cb.message.edit_text(
            f"✅ Успешное делегирование `{data['energy']}` ENERGY на `{data['to_address']}`\n"
            f"TX ID: `{txid}`"
        )

    except Exception as e:
        logger.exception(f"❌ Ошибка при делегировании user_id={uid}")
        await cb.message.edit_text(f"❌ Ошибка при делегировании:\n`{escape(str(e))}`")
    finally:
        await state.clear()
