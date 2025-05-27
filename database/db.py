from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import datetime
import os

from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./devatapath.db")
Base        = declarative_base()
engine      = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, index=True, nullable=False)
    course_id  = Column(String, nullable=False)
    starts_at  = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    active     = Column(Boolean, default=True, nullable=False)

class PaymentProof(Base):
    __tablename__ = "payment_proofs"
    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, index=True, nullable=False)
    course_id = Column(String, nullable=False)
    file_id   = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status    = Column(String, default="pending", nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)