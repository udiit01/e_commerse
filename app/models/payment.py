from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float, nullable=False)
    provider = Column(String(100))  # e.g., stripe
    provider_payment_id = Column(String(255), nullable=True)
    status = Column(String(50), default="initiated")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
