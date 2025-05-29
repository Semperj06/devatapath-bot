# Подключаем библиотеку для асинхронного запуска функций и воркера бота
import asyncio
import logging

# Импортируем класс Bot для работы с Telegram Bot API и диспетчер для маршрутизации сообщений
from aiogram import Bot, Dispatcher

# Импортируем токен вашего бота из файла конфигурации (config.py)
from app.core.settings import settings

# Подключаем модуль-обработчик для команды /start
from app.bot.handlers.menu_handlers import router as menu_router
from app.bot.handlers.course_select import router as course_router
from app.bot.handlers.start import router as start_router
from app.bot import bot, dp
from app.bot.handlers.payment import router as payment_router
from app.bot.handlers.admin import router as admin_router

# -------------------- Настройка бота и диспетчера --------------------

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

async def on_startup():
    # 1) Удаляем все вебхуки (и сбрасываем очередные апдейты)
    await bot.delete_webhook(drop_pending_updates=True)

    # 2) Инициализируем БД, логгеры, и т.п.
    from app.db.base import init_db
    init_db()

    print("Бот запущен и готов принимать команды")

async def main():
    # регистрируем все роутеры
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(course_router)
    dp.include_router(payment_router)
    dp.include_router(admin_router)

    # регистрируем on_startup —
    dp.startup.register(on_startup)

    # запускаем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
