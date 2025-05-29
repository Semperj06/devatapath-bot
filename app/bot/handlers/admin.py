# app/bot/handlers/admin.py

from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

from app.core.settings import settings
from app.db.base       import SessionLocal
from app.db.models     import PaymentProof, Subscription

router = Router()

@router.callback_query(lambda c: c.data.startswith("approve_"))
async def on_approve(call: types.CallbackQuery):
    proof_id = int(call.data.split("_", 1)[1])
    with SessionLocal() as db:
        proof = db.get(PaymentProof, proof_id)
        proof.status = "approved"
        sub = Subscription(
            user_id=proof.user_id,
            course_id=proof.course_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
        )
        db.add(sub)
        db.commit()

    await call.answer("Оплата подтверждена ✅")
    await call.bot.send_message(
        proof.user_id,
        "✅ Ваша оплата подтверждена — доступ открыт!"
    )

@router.callback_query(lambda c: c.data.startswith("reject_"))
async def on_reject(call: types.CallbackQuery):
    proof_id = int(call.data.split("_", 1)[1])
    with SessionLocal() as db:
        proof = db.get(PaymentProof, proof_id)
        proof.status = "rejected"
        db.commit()

    await call.answer("Скриншот отклонён ❌")
    await call.bot.send_message(
        proof.user_id,
        "❌ Скриншот отклонён — пришлите, пожалуйста, новый."
    )