import os, json
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    ADMIN_ID: int
    MINI_COURSES_FILE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# сразу читаем JSON и сохраняем в отдельную переменную MINI_COURSES
with open(settings.MINI_COURSES_FILE, encoding="utf-8") as f:
    MINI_COURSES = json.load(f)



