from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Subscription(Base):
    __tablename__ = "subscriptions"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, index=True, nullable=False)
    course_id  = Column(String, nullable=False)
    # теперь правильно вызываем utcnow() класса datetime
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date   = Column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"<Subscription(id={self.id}, user_id={self.user_id},"
            f" course_id='{self.course_id}', start_date={self.start_date},"
            f" end_date={self.end_date})>"
        )


class PaymentProof(Base):
    __tablename__ = "payment_proofs"

    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, index=True, nullable=False)
    course_id = Column(String, nullable=False)
    file_id   = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  # исправлено
    status    = Column(String, nullable=False, default="pending")

    def __repr__(self):
        return (
            f"<PaymentProof(id={self.id}, user_id={self.user_id},"
            f" course_id='{self.course_id}', status='{self.status}',"
            f" timestamp={self.timestamp})>"
        )


class ProofHistory(Base):
    __tablename__ = "proof_history"

    id        = Column(Integer, primary_key=True)
    proof_id  = Column(Integer, ForeignKey("payment_proofs.id"), nullable=False)
    action    = Column(String, nullable=False)  # 'approved' или 'rejected'
    admin_id  = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  # и тут тоже

    proof     = relationship("PaymentProof", back_populates="history")


PaymentProof.history = relationship(
    "ProofHistory", order_by=ProofHistory.id, back_populates="proof"
)