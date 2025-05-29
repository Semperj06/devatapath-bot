# app/bot/handlers/payment.py

import datetime
from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from app.core.settings       import settings, MINI_COURSES
from app.bot.handlers.states import PaymentStates
from app.db.base             import SessionLocal
from app.db.models           import PaymentProof, Subscription
from app.keyboards.menu      import main_menu

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("pay_"))
async def ask_confirm_payment(call: types.CallbackQuery, state: FSMContext):
    await call.answer()  # убираем “крутилку”
    course_id = call.data.split("_", 1)[1]
    course = MINI_COURSES.get(course_id)
    if not course:
        return await call.message.answer("❌ Курс не найден.")

    # 1) Ссылка на оплату
    await call.message.answer(
        f"Перейдите по ссылке, чтобы оплатить *{course['title']}* за {course['price']}₽:\n{course['pay_link']}",
        parse_mode="Markdown"
    )

    # 2) Предлагаем кнопку “Я оплатил”
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Я оплатил", callback_data=f"paid_{course_id}")
    kb.adjust(1)
    await call.message.answer(
        "После оплаты нажмите кнопку ниже и пришлите скриншот оплаты.",
        reply_markup=kb.as_markup()
    )

    # 3) Входим в FSM
    await state.update_data(course_id=course_id)
    await state.set_state(PaymentStates.waiting_for_screenshot)


@router.callback_query(lambda c: c.data and c.data.startswith("paid_"))
async def on_paid_button(call: types.CallbackQuery):
    await call.answer()  # убираем “крутилку”
    # удаляем старую клавиатуру и просим фото
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("📸 Пришлите, пожалуйста, скриншот вашей оплаты.")


@router.message(
    StateFilter(PaymentStates.waiting_for_screenshot),
    lambda m: bool(m.photo)
)
async def receive_screenshot(message: types.Message, state: FSMContext):
    data      = await state.get_data()
    course_id = data["course_id"]
    user_id   = message.from_user.id
    file_id   = message.photo[-1].file_id
    ts        = datetime.datetime.utcnow()

    # 1) Сохраняем запись в БД
    with SessionLocal() as db:
        proof = PaymentProof(
            user_id=user_id,
            course_id=course_id,
            file_id=file_id,
            timestamp=ts,
            status="pending"
        )
        db.add(proof)
        db.commit()
        db.refresh(proof)

    # 2) Пересылаем фото в админ-группу с кнопками
    admin_kb = InlineKeyboardBuilder()
    admin_kb.button(text="✅ Одобрить", callback_data=f"approve_{proof.id}")
    admin_kb.button(text="❌ Отклонить", callback_data=f"reject_{proof.id}")
    # кнопка для перехода в диалог с пользователем
    admin_kb.button(
        text="🔗 Профиль",
        url=f"tg://user?id={proof.user_id}")
    admin_kb.adjust(3)

    await message.bot.send_photo(
        chat_id=settings.ADMIN_CHAT_ID,
        photo=file_id,
        caption=(
            f"Новый скрин #{proof.id} курса «{proof.course_id}»\n"
            f"от пользователя {proof.user_id}"
        ),
        reply_markup=admin_kb.as_markup()
    )

    # 3) Уведомляем пользователя и возвращаем главное меню
    await message.answer(
        "✅ Скриншот отправлен администраторам на проверку.",
        reply_markup=main_menu()
    )
    await state.clear()