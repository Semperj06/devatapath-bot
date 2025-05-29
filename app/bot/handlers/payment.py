import datetime
from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from app.core.settings      import MINI_COURSES
from app.bot.handlers.states import PaymentStates
from app.db.base            import SessionLocal
from app.db.models          import PaymentProof
from app.keyboards.menu import main_menu
router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("pay_"))
async def ask_confirm_payment(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    course_id = call.data.split("_", 1)[1]
    course = MINI_COURSES.get(course_id)
    if not course:
        return await call.message.answer("❌ Курс не найден.")

    # 1) Шлём ссылку
    await call.message.answer(
        f"Перейдите по ссылке, чтобы оплатить *{course['title']}* за {course['price']}₽:\n"
        f"{course['pay_link']}",
        parse_mode="Markdown"
    )
    # 2) Предлагаем прислать скрин через callback
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Я оплатил", callback_data=f"paid_{course_id}")
    kb.adjust(1)
    await call.message.answer(
        "После оплаты нажмите кнопку и пришлите скриншот:",
        reply_markup=kb.as_markup()
    )

    await state.update_data(course_id=course_id)
    await state.set_state(PaymentStates.waiting_for_screenshot)


@router.callback_query(lambda c: c.data and c.data.startswith("paid_"))
async def on_paid_button(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("📸 Пришлите, пожалуйста, скриншот вашей оплаты.")
    # FSM-состояние оставить прежним: PaymentStates.waiting_for_screenshot


@router.message(
    StateFilter(PaymentStates.waiting_for_screenshot),
    lambda m: bool(m.photo)
)
async def receive_screenshot(message: types.Message, state: FSMContext):
    data      = await state.get_data()
    course_id = data["course_id"]
    proof_time= datetime.datetime.utcnow()
    user_id   = message.from_user.id
    file_id   = message.photo[-1].file_id

    with SessionLocal() as db:
        db.add(PaymentProof(
            user_id=user_id,
            course_id=course_id,
            file_id=file_id,
            timestamp=proof_time,
            status="pending"
        ))
        db.commit()

    await message.answer(
        "✅ Скриншот получен! Проверим и дадим доступ.",
        reply_markup=main_menu()
    )
    await state.clear()