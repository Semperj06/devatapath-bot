# handlers/course_select.py

from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.menu import main_menu        # твоя функция для главного меню (не меняли)
from config import MINI_COURSES             # словарь с данными о мини-курсах

router = Router()  # отдельный роутер для мини-курсов


@router.callback_query(lambda c: c.data and c.data.startswith("mini_"))
async def mini_detail(callback: types.CallbackQuery):
    """
    1) Ловим нажатие на inline-кнопку mini_X
    2) Собираем описание курса и кнопку «Оплатить» + «Назад к списку»
    3) Редактируем текст того же сообщения
    """
    # 1) убираем «крутилку»
    await callback.answer()

    # 2) получаем ID курса
    course_id = callback.data.split("_", 1)[1]
    course = MINI_COURSES.get(course_id)
    if not course:
        return await callback.message.answer("❌ Ошибка: курс не найден.")

    # 3) текст с описанием
    text = (
        f"*{course['title']}*\n\n"
        f"{course['desc']}\n\n"
        f"*Цена:* {course['price']} ₽\n\n"
        "Выберите действие:"
    )

    # 4) билдим inline-клавиатуру
    builder = InlineKeyboardBuilder()
    # 5) кнопка оплаты
    builder.button(
        text="💳 Оплатить",
        callback_data=f"pay_{course_id}"
    )
    # 6) кнопка «назад к списку»
    builder.button(
        text="◀️ Назад к списку",
        callback_data="back_to_mini_list"
    )
    # 7) один столбик кнопок
    builder.adjust(1)
    kb = builder.as_markup()

    # 8) редактируем предыдущее сообщение
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=kb
    )


@router.callback_query(lambda c: c.data == "back_to_mini_list")
async def back_to_list_handler(callback: types.CallbackQuery):
    """
    Обработчик для кнопки ◀️ Назад к списку.
    Просто вызываем тот же хендлер, что показывает список.
    """
    await callback.answer()  # убираем «крутилку»

    # импорт здесь, чтобы не было циклических зависимостей при старте
    from handlers.menu_handlers import mini_courses_handler

    # mini_courses_handler ожидает Message, а у нас CallbackQuery, поэтому
    # передаем callback.message
    await mini_courses_handler(callback.message)


@router.callback_query(lambda c: c.data and c.data.startswith("pay_"))
async def pay_handler(callback: types.CallbackQuery):
    """
    Обработчик «Оплатить». Берем ссылку из MINI_COURSES и шлем юзеру.
    """
    await callback.answer()
    course_id = callback.data.split("_", 1)[1]
    course = MINI_COURSES.get(course_id)
    if not course:
        return await callback.message.answer("❌ Курс не найден.")

    # Если у тебя в config.py ключ называется 'link' или 'pay_link',
    # проверь чтобы словарь MINI_COURSES тоже содержал этот ключ!
    pay_link = course.get("pay_link") or course.get("link")
    if not pay_link:
        return await callback.message.answer("❌ Ссылка для оплаты не задана.")

    await callback.message.answer(
        f"💳 Чтобы оплатить *{course['title']}*, перейдите по ссылке:\n\n"
        f"{pay_link}",
        parse_mode="Markdown",
        reply_markup=main_menu()  # возвращаем в главное меню
    )



@router.callback_query(lambda c: c.data and c.data.startswith("mini_"))
async def mini_detail(callback: types.CallbackQuery):
    # 1) подтверждаем callback (убираем кружок)
    await callback.answer()

    # 2) получаем ID курса
    course_id = callback.data.split("_", 1)[1]
    course = MINI_COURSES.get(course_id)
    if not course:
        return await callback.message.answer("❌ Ошибка: курс не найден.")

    # 3) подготавливаем текст описания
    text = (
        f"*{course['title']}*\n\n"
        f"{course['desc']}\n\n"
        f"*Цена:* {course['price']} ₽\n\n"
        "Выберите действие ниже:"
    )

    # 4) билдeр inline-клавиатуры
    builder = InlineKeyboardBuilder()
    # кнопка со ссылкой на оплату
    builder.button(
        text="💳 Оплатить",
        url=course['pay_link']
    )
    # кнопка "Я оплатил" для загрузки скрина
    builder.button(
        text="✅ Я оплатил",
        callback_data=f"paid_{course_id}"
    )
    # вернёмся в главное меню
    builder.button(
        text="🏠 Главное меню",
        callback_data="show_main_menu"
    )
    # размещаем по одной кнопке в строке
    builder.adjust(1)

    # 5) генерируем разметку и отправляем
    kb = builder.as_markup()
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=kb
    )