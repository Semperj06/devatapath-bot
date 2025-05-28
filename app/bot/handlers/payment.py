# app/bot/handlers/payment.py

import datetime
from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from app.core.settings import settings, MINI_COURSES        # <<< именно он!
from app.keyboards.menu    import main_menu
from app.db.base           import SessionLocal
from app.db.models         import PaymentProof, Subscription
from app.bot.handlers.states import PaymentStates

router = Router()


# 1) Обработчик кнопки «Оплатить» из меню курсов
@router.callback_query(lambda c: c.data and c.data.startswith("pay_"))
async def ask_confirm_payment(call: types.CallbackQuery, state: FSMContext):
    print("🔥 ask_confirm_payment вызван, callback_data =", call.data)
    await call.answer()
    course_id = call.data.split("_", 1)[1]

    # достаём данные курса
    course = MINI_COURSES.get(course_id)
    if not course:
        return await call.message.answer("❌ Курс не найден.")

    # 1.1) сначала даём ссылку на оплату
    await call.message.answer(
        f"Перейдите по ссылке, чтобы оплатить курс *{course['title']}* за {course['price']}₽:\n\n"
        f"{course['pay_link']}",
        parse_mode="Markdown"
    )

    # 1.2) потом предлагаем кнопку «Я оплатил»
    kb = InlineKeyboardBuilder().button(
        text="✅ Я оплатил",
        callback_data=f"paid_{course_id}"
    ).as_markup()

    await call.message.answer(
        "После оплаты нажмите кнопку ниже и пришлите скриншот платежа:",
        reply_markup=kb
    )

    # 1.3) сохраняем в FSM, какой курс выбрали, и переводим в состояние ожидания фото
    await state.update_data(course_id=course_id)
    await state.set_state(PaymentStates.waiting_for_screenshot)


# 2) Обработчик нажания «✅ Я оплатил» — просто подтверждаем, а сам скрин ждём в сообщении
@router.callback_query(lambda c: c.data and c.data.startswith("paid_"))
async def on_paid_button(call: types.CallbackQuery):
    await call.answer()  # убираем «крутилку»
    # можно удалить клаву, чтобы не нажать дважды
    await call.message.edit_reply_markup(reply_markup=None)


# 3) Приём скриншота в состоянии FSMStates.waiting_for_screenshot
@router.message(
    StateFilter(PaymentStates.waiting_for_screenshot),
    lambda message: bool(message.photo)  # пропускаем только фото
)
async def receive_screenshot(message: types.Message, state: FSMContext):
    data = await state.get_data()
    course_id = data['course_id']
    user_id   = message.from_user.id
    file_id   = message.photo[-1].file_id
    ts        = datetime.datetime.utcnow()

    # Сохраняем платежное доказательство
    with SessionLocal() as session:
        proof = PaymentProof(
            user_id=user_id,
            course_id=course_id,
            file_id=file_id,
            timestamp=ts,
            status="pending"
        )
        session.add(proof)
        session.commit()

    # Ответ пользователю и возврат в главное меню
    await message.answer(
        "✅ Спасибо! Ваш скриншот получен, мы проверим его и дадим вам доступ к курсу.",
        reply_markup=main_menu()
    )
    # сбрасываем FSM
    await state.clear()
