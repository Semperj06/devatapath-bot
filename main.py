# main.py
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.menu_handlers import router as menu_router
from handlers.course_select import router as course_router
from handlers.payment import router as payment_router

# Импортируем init_db
from database.db import init_db

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher()

async def on_startup() -> None:
    """
    Выполняется один раз при старте polling.
    Здесь инициализируем базу и любые другие «разовые» задачи.
    """
    init_db()
    print("✅ Синхронная БД готова!")

async def main() -> None:
    # Регистрируем все роутеры
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(course_router)
    dp.include_router(payment_router)

    # Регистрируем хук старта
    dp.startup.register(on_startup)

    # Запускаем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

