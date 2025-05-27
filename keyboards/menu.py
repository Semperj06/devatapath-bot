# Главное меню с кнопками
# keyboards/menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="📚 Мини-курсы"),
            KeyboardButton(text="🎓 Продвинутые курсы"),
        ],
        [
            KeyboardButton(text="🎁 Безоплатные"),
            KeyboardButton(text="📖 Книги"),
        ],
        [
            KeyboardButton(text="🔓 Мои курсы"),
            KeyboardButton(text="💖 Поддержать проект"),
        ],
        [
            KeyboardButton(text="🤝 Служба заботы"),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,       # передаём список рядов
        resize_keyboard=True,   # подгонять размер под кнопки
    )

