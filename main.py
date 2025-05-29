# main.py
import asyncio, logging
from aiogram import Bot, Dispatcher

from app.core.settings import settings
from app.bot.handlers.menu_handlers import router as menu_router
from app.bot.handlers.course_select import router as course_router
from app.bot.handlers.start import router as start_router
from app.bot.handlers.payment import router as payment_router
from app.bot.handlers.admin import router as admin_router

bot = Bot(token=settings.BOT_TOKEN)
dp  = Dispatcher()

async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    from app.db.base import init_db
    init_db()
    logging.getLogger().info("Бот запущен и готов принимать команды")

async def main():
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(course_router)
    dp.include_router(payment_router)
    dp.include_router(admin_router)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
