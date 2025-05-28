# database/db.py
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

# 📦 Базовый класс для всех моделей
Base = declarative_base()

# ⚙️ Синхронный движок
engine = create_engine(
    DATABASE_URL,        # например "sqlite:///./devatapath.db"
    echo=False,          # отключаем вывод SQL в консоль
    future=True,         # API SQLAlchemy 2.x
)

# 🔌 Фабрика сессий
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

def init_db() -> None:
    """
    Создаёт все таблицы, описанные в моделях, если их ещё нет.
    Вызывается один раз при старте приложения.
    """
    Base.metadata.create_all(bind=engine)
