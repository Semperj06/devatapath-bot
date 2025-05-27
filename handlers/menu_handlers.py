from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder  # Builder для inline-клавиатур
from keyboards.menu import main_menu                        # твоя функция для главного меню

router = Router()

@router.message(lambda m: m.text == "🎓 Продвинутые курсы")
async def advanced_courses_handler(message: types.Message):
    # заглушка — замените на свой список
    await message.answer(
        "🎓 *Продвинутые курсы* 🎓\n\n"
        "1) Полный курс по Цигун\n"
        "2) Глубокая практика медитаций\n\n"
        "Нажмите цифру или вернитесь назад.",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@router.message(lambda m: m.text == "🎁 Безоплатные")
async def free_practices_handler(message: types.Message):
    await message.answer(
        "🔹 *Бесплатные практики* 🔹\n\n"
        "1) Медитация на заземление\n"
        "2) Цигун-паузы в течение дня\n"
        "3) Визуализация гармонизации энергий\n\n"
        "Нажмите цифру, чтобы получить детали, или /start для меню.",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@router.message(lambda m: m.text == "📖 Книги")
async def books_handler(message: types.Message):
    await message.answer(
        "📖 *Рекомендации книг* 📖\n\n"
        "1) «Путь Цигун» — Автор A\n"
        "2) «Иннер Девата» — Автор B\n"
        "3) «Энергетика тела» — Автор C\n\n"
        "Вернитесь назад или /start.",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@router.message(lambda m: m.text == "🔒 Мои курсы")
async def my_courses_handler(message: types.Message):
    await message.answer(
        "🔒 У вас пока нет активных курсов.\n"
        "После оплаты они появятся здесь.",
        reply_markup=main_menu()
    )

@router.message(lambda m: m.text == "💖 Поддержать проект")
async def donate_handler(message: types.Message):
    await message.answer(
        "🙏 Спасибо за желание поддержать проект!\n"
        "Перейдите по ссылке, чтобы оставить донат: https://t.me/Tribute",
        reply_markup=main_menu()
    )

@router.message(lambda m: m.text == "🤝 Служба заботы")
async def support_handler(message: types.Message):
    await message.answer(
        "🤝 *Служба заботы*\n\n"
        "Если нужна помощь — пишите на support@domain.com\n"
        "Или заходите в наш чат поддержки: https://t.me/YourSupportChat",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@router.message(lambda message: message.text == "📚 Мини-курсы")
async def mini_courses_handler(message: types.Message):
    """
    Обработчик кнопки "Мини-курсы".
    Отправляет текст с перечнем курсов и inline-кнопки для выбора.
    """

    # 1) Готовим текст
    text = (
        "🔹 *Мини-курсы* 🔹\n\n"
        "Выберите курс:\n"
    )

    # 2) Создаём билдер — в него будем «тыкать» наши кнопки
    builder = InlineKeyboardBuilder()

    # 3) Добавляем кнопки курсов (они станут в одну колонку, т.к. потом adjust(1))
    builder.button(
        text="1️⃣ Основы дыхания",
        callback_data="mini_1"  # здесь ID первого мини-курса
    )
    builder.button(
        text="2️⃣ Утренняя энергетическая зарядка",
        callback_data="mini_2"
    )
    builder.button(
        text="3️⃣ Простые Qigong-упражнения",
        callback_data="mini_3"
    )

    # 4) Настраиваем, чтобы по 1 кнопке в строке
    builder.adjust(1)

    """# 5) Навигационные кнопки
    builder.button(
        text="◀️ Назад",
        callback_data="back_to_menu"  # вернёмся в главное меню
    )
    builder.button(
        text="🏠 Главное меню",
        callback_data="show_main_menu"
    )"""

    # 6) Две кнопки в строке
    builder.adjust(2)

    # 7) Превращаем билдер в готовый объект InlineKeyboardMarkup
    kb = builder.as_markup()

    # 8) Шлём ответ
    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=kb  # вот наша клавиатура
    )
