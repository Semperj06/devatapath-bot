import json, os
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env
# app/core/config.py
import os, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # подхватываем .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devatapath.db")

# загружаем мини-курсы из внешнего файла
COURSE_FILE = os.path.join(os.path.dirname(__file__), "mini_courses.json")
with open(COURSE_FILE, encoding="utf-8") as f:
    MINI_COURSES = json.load(f)

