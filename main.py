# Подключаем библиотеку для асинхронного запуска функций и воркера бота
import asyncio
import logging

# Импортируем класс Bot для работы с Telegram Bot API и диспетчер для маршрутизации сообщений
from aiogram import Bot, Dispatcher

# Импортируем токен вашего бота из файла конфигурации (config.py)
from app.core.settings import settings, MINI_COURSES

# Подключаем модуль-обработчик для команды /start
from app.bot.handlers.menu_handlers import router as menu_router
from app.bot.handlers.course_select import router as course_router
from app.bot.handlers.payment import router as payment_router
from app.bot.handlers.start import router as start_router
from app.db.base import init_db


# -------------------- Настройка бота и диспетчера --------------------

# Создаём экземпляр бота: указываем токен, полученный от BotFather
bot = Bot(token=settings.BOT_TOKEN)
# Создаём диспетчер, который будет «ловить» все входящие обновления
dp = Dispatcher()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# -------------------- Функция при старте --------------------
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    init_db()
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
