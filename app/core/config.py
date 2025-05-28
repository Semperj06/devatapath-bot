import os
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env
# app/core/config.py
import os, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # подхватываем .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# загружаем мини-курсы из внешнего файла
_config_dir = Path(__file__).parent
with open(_config_dir / "mini_courses.json", encoding="utf-8") as f:
    MINI_COURSES = json.load(f)