from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devatapath.db")



MINI_COURSES = {
    "1": {
        "title":    "Основы дыхания",
        "desc":     "В этом курсе вы научитесь основам осознанного дыхания...",
        "price":    "199 ₽",
        "pay_link":     "https://pay.example.com/course1"
    },
    "2": {
        "title":    "Утренняя энергетическая зарядка",
        "desc":     "Утренний комплекс упражнений для бодрости и энергии...",
        "price":    "299 ₽",
        "pay_link":     "https://pay.example.com/course2"
    },
    "3": {
        "title":    "Простые Qigong-упражнения",
        "desc":     "Набор базовых упражнений цигун для начинающих...",
        "price":    "249 ₽",
        "pay_link":     "https://pay.example.com/course3"
    },
}