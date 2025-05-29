# app/bot/handlers/admin.py
from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta


from aiogram.filters import Command
from app.core.settings import settings
from app.db.base       import SessionLocal
from app.db.models     import PaymentProof, Subscription

router = Router()


@router.message(lambda m: m.photo)
async def forward_to_admin(message: types.Message):
    # ... ваш код пересылки скрина ...

    # В ответ пользователю:
    await message.answer("✅ Скриншот отправлен на проверку администраторам.")


@router.callback_query(lambda c: c.data.startswith("approve_"))
async def on_approve(call: types.CallbackQuery):
    proof_id = int(call.data.split("_", 1)[1])

    # 1) внутри сессии обновляем статус и создаём подписку
    with SessionLocal() as db:
        proof = db.get(PaymentProof, proof_id)
        # Сразу забираем user_id и course_id
        user_id   = proof.user_id
        course_id = proof.course_id

        proof.status = "approved"
        sub = Subscription(
            user_id=user_id,
            course_id=course_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
        )
        db.add(sub)
        db.commit()

    # 2) за пределами сессии используем сохранённый user_id
    await call.answer("✅ Оплата подтверждена")
    await call.bot.send_message(
        chat_id=user_id,
        text="✅ Ваша оплата подтверждена, доступ к курсу открыт!"
    )


@router.callback_query(lambda c: c.data.startswith("reject_"))
async def on_reject(call: types.CallbackQuery):
    proof_id = int(call.data.split("_", 1)[1])

    # 1) внутри сессии меняем статус
    with SessionLocal() as db:
        proof = db.get(PaymentProof, proof_id)
        user_id = proof.user_id  # сразу забираем user_id
        proof.status = "rejected"
        db.commit()

    # 2) за пределами сессии уведомляем пользователя
    await call.answer("❌ Скриншот отклонён")
    await call.bot.send_message(
        chat_id=user_id,
        text="❌ Ваш скриншот отклонён, пришлите, пожалуйста, новый."
    )


@router.message(Command("queue"))
async def show_queue(message: types.Message):
    """
    /queue — показать все pending-запросы
    """
    with SessionLocal() as db:
        pendings = (
            db.query(PaymentProof)
              .filter_by(status="pending")
              .order_by(PaymentProof.id)
              .all()
        )

    if not pendings:
        return await message.answer("📭 Очередь пуста.")

    text = "\n".join(
        f"#{p.id} от {p.user_id} для курса {p.course_id}"
        for p in pendings
    )
    await message.answer(f"📋 В очереди:\n{text}")


@router.callback_query(lambda c: c.data.startswith("cancelsub_"))
async def on_cancel_sub(call: types.CallbackQuery):
    """
    callback_data = "cancelsub_{user_id}"
    """
    user_id = int(call.data.split("_", 1)[1])
    with SessionLocal() as db:
        sub = db.query(Subscription).filter_by(user_id=user_id).first()
        if not sub:
            return await call.answer("❗ У этого пользователя нет подписки", show_alert=True)
        db.delete(sub)
        db.commit()

    await call.answer("🗑 Подписка отменена")
    await call.bot.send_message(
        user_id,
        "⚠️ Ваша подписка отменена администратором."
    )


# Клавиатура для отмены подписки (можно встроить в любой ваш админ-репорт)
def cancel_sub_kb(user_id: int) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="✂️ Отменить подписку",
        callback_data=f"cancelsub_{user_id}"
    )
    kb.adjust(1)
    return kb.as_markup()