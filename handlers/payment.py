from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import MINI_COURSES
from database.db import SessionLocal, PaymentProof
from keyboards.menu import main_menu
import datetime
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import StatesGroup, State


router = Router()

# 1) Объявляем FSM-класс с единственным состоянием
class PaymentStates(StatesGroup):
    waiting_for_screenshot = State()

# 2) Обработчик кнопки «Оплатить» → предлагаем нажать «Я оплатил»
@router.callback_query(lambda c: c.data and c.data.startswith("pay_"))
async def ask_confirm_payment(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    course_id = call.data.split("_", 1)[1]
    course = MINI_COURSES.get(course_id)
    if not course:
        return await call.message.answer("❌ Курс не найден.")

    # 2.1) Строим клавиатуру с кнопкой «Я оплатил»
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Я оплатил",
        callback_data=f"paid_{course_id}"
    )
    builder.adjust(1)
    kb = builder.as_markup()

    # 2.2) Отправляем запрос скрина и клавиатуру
    await call.message.answer(
        "После оплаты нажмите кнопку «Я оплатил» и пришлите скриншот оплаты.",
        reply_markup=kb
    )

    # 2.3) Переходим в состояние ожидания скрина
    await state.update_data(course_id=course_id)
    await state.set_state(PaymentStates.waiting_for_screenshot)

# 3) Обработчик нажатия «Я оплатил» → просим прислать фото
@router.callback_query(lambda c: c.data and c.data.startswith("paid_"))
async def paid_handler(call: types.CallbackQuery):
    # Нам уже не нужен здесь state, просто убираем «крутилку»
    await call.answer()

# 4) Приём скриншота в том состоянии
@router.message(
    StateFilter(PaymentStates.waiting_for_screenshot),
    lambda message: bool(message.photo)
)
async def receive_screenshot(message: types.Message, state: FSMContext):
    data = await state.get_data()
    course_id = data['course_id']
    user_id   = message.from_user.id
    file_id   = message.photo[-1].file_id

    # Сохраняем скрин в таблицу PaymentProof
    with SessionLocal() as session:
        proof = PaymentProof(
            user_id=user_id,
            course_id=course_id,
            file_id=file_id,
            timestamp=datetime.datetime.utcnow(),
            status="pending"
        )
        session.add(proof)
        session.commit()

    await message.answer(
        "✅ Спасибо, скриншот получен! Мы проверим его и дадим вам доступ к курсу.",
        reply_markup=main_menu()
    )
    await state.clear()
