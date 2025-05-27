# handlers/start.py
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.menu import main_menu

router = Router()                                    # ← вот он!

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать! Здесь ты найдёшь практики, мини-курсы и многое другое.",
        reply_markup=main_menu()
    )
