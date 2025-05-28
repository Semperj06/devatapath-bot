# app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime
from .base import Base
import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"
    id  = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    course_id= Column(String,  nullable=False)
    start = Column(DateTime, default=datetime.datetime.utcnow)
    end = Column(DateTime)

class PaymentProof(Base):
    __tablename__ = "payment_proofs"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, index=True, nullable=False)
    course_id  = Column(String,  nullable=False)
    file_id    = Column(String,  nullable=False)
    timestamp  = Column(DateTime, default=datetime.datetime.utcnow)
    status     = Column(String,  nullable=False)  # e.g. "pending", "approved"

