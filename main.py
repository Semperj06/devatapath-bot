# Подключаем библиотеку для асинхронного запуска функций и воркера бота
import asyncio

# Импортируем класс Bot для работы с Telegram Bot API и диспетчер для маршрутизации сообщений
from aiogram import Bot, Dispatcher

# Импортируем токен вашего бота из файла конфигурации (config.py)
from config import BOT_TOKEN

# Подключаем модуль-обработчик для команды /start
from handlers.start import router as start_router
from handlers.menu_handlers import router as menu_router
from handlers.course_select import router as course_router
from database.db import init_db
from handlers.payment import router as payment_router



# -------------------- Настройка бота и диспетчера --------------------

# Создаём экземпляр бота: указываем токен, полученный от BotFather
bot = Bot(token=BOT_TOKEN)

# Создаём диспетчер, который будет «ловить» все входящие обновления
dp = Dispatcher()

# -------------------- Функция при старте --------------------
async def on_startup():
    init_db()
    """
    Эта функция выполняется один раз при запуске поллинга.
    Здесь можно выполнить инициализацию: логирование, проверка БД и т.д.
    """
    print("Бот запущен и готов принимать команды")

# -------------------- Основная корутина --------------------
async def main():
    """
    Главная точка запуска нашего бота.
    Регистрируем роутеры и стартуем поллинг.
    """
    # Регистрируем роутер из модуля handlers.start, чтобы /start обрабатывался
    dp.include_router(start_router)
    dp.include_router(menu_router)
    # Регистрируем наш on_startup для вывода сообщения о старте в консоль
    dp.startup.register(on_startup)
    dp.include_router(course_router)
    dp.include_router(payment_router)
    # Запускаем «долгий» метод запуска бота через поллинг
    # Благодаря await, event loop не блокируется
    await dp.start_polling(bot)

# -------------------- Запуск скрипта --------------------
if __name__ == "__main__":
    # asyncio.run() автоматически создаёт и закрывает event loop
    asyncio.run(main())
