# app/core/settings.py
import os
import json
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# подгружаем .env в os.environ
load_dotenv()


class Settings(BaseSettings):
    # обязательные поля
    BOT_TOKEN: str
    DATABASE_URL: str  # например, sqlite:///./devatapath.db
    ADMIN_ID: int       # если вы хотите хранить айди админа
    MINI_COURSES_FILE: str  # путь к JSON-файлу с описанием курсов

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# единый экземпляр настроек для всего проекта
settings = Settings()

# сразу загружаем JSON с мини-курсами
with open(settings.MINI_COURSES_FILE, encoding="utf-8") as f:
    MINI_COURSES_FILE = json.load(f)



