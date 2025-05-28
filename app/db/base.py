# database/db.py
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.settings import settings

# 📦 Базовый класс для всех моделей
Base = declarative_base()
url = settings.DATABASE_URL
engine = create_engine(url, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db() -> None:
    # import all your models so that Base.metadata knows about them
    from app.db.models import Subscription, PaymentProof
    Base.metadata.create_all(bind=engine)
