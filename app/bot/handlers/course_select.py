from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards.menu import main_menu
from app.core.settings import MINI_COURSES

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("mini_"))
async def mini_detail(callback: types.CallbackQuery):
    await callback.answer()
    course_id = callback.data.split("_", 1)[1]
    course = MINI_COURSES.get(course_id)
    if not course:
        return await callback.message.answer("❌ Ошибка: курс не найден.")

    text = (
        f"*{course['title']}*\n\n"
        f"{course['desc']}\n\n"
        f"*Цена:* {course['price']} ₽\n\n"
        "Выберите действие:"
    )

    builder = InlineKeyboardBuilder()
    # 1) кнопка «Оплатить» теперь не URL, а callback
    builder.button(
        text="💳 Оплатить",
        callback_data=f"pay_{course_id}"
    )
    # 2) «Назад к списку»
    builder.button(
        text="◀️ Назад к списку",
        callback_data="back_to_mini_list"
    )
    builder.adjust(1)  # по одной в строке

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == "back_to_mini_list")
async def back_to_list_handler(callback: types.CallbackQuery):
    await callback.answer()
    from app.bot.handlers.menu_handlers import mini_courses_handler
    await mini_courses_handler(callback.message)