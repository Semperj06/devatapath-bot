# app/bot/handlers/admin.py

from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime      import datetime, timedelta

from app.bot           import bot
from app.core.settings import settings
from app.db.base       import SessionLocal
from app.db.models     import PaymentProof, Subscription

router = Router()


@router.message(lambda m: m.photo)
async def forward_to_admin(message: types.Message):
    """
    Пересылает присланный пользователем скрин в группу-админку
    с кнопками Одобрить/Отклонить.
    """
    # 1) Получаем последнюю запись PaymentProof
    with SessionLocal() as db:
        proof = (
            db.query(PaymentProof)
              .order_by(PaymentProof.id.desc())
              .first()
        )

    # 2) Собираем клавиатуру для админов
    kb = InlineKeyboardBuilder()
    kb.button("✅ Одобрить", callback_data=f"approve_{proof.id}")
    kb.button("❌ Отклонить", callback_data=f"reject_{proof.id}")
    kb.adjust(2)

    # 3) Пересылаем фото и текст в админ-чат
    await bot.send_photo(
        chat_id=settings.ADMIN_CHAT_ID,
        photo=message.photo[-1].file_id,
        caption=(
            f"Новый скрин #{proof.id} курса {proof.course_id} "
            f"от пользователя {proof.user_id}"
        ),
        reply_markup=kb.as_markup()
    )

    # 4) Уведомляем пользователя
    await message.answer("✅ Скриншот отправлен на проверку администраторам.")



@router.callback_query(lambda c: c.data.startswith("approve_"))
async def on_approve(call: types.CallbackQuery):
    proof_id = int(call.data.split("_", 1)[1])
    with SessionLocal() as db:
        proof = db.get(PaymentProof, proof_id)
        proof.status = "approved"
        # создаём подписку на 30 дней
        sub = Subscription(
            user_id=proof.user_id,
            course_id=proof.course_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
        )
        db.add(sub)
        db.commit()

    await call.answer("Оплата подтверждена ✅")
    await bot.send_message(
        proof.user_id,
        "✅ Ваша оплата подтверждена, доступ к курсу открыт!"
    )


@router.callback_query(lambda c: c.data.startswith("reject_"))
async def on_reject(call: types.CallbackQuery):
    proof_id = int(call.data.split("_", 1)[1])
    with SessionLocal() as db:
        proof = db.get(PaymentProof, proof_id)
        proof.status = "rejected"
        db.commit()

    await call.answer("Скриншот отклонён ❌")
    await bot.send_message(
        proof.user_id,
        "❌ Ваш скриншот отклонён, пришлите, пожалуйста, новый."
    )