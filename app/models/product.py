from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum
from db.base import Base
from datetime import datetime
import enum


class ProductType(enum.Enum):
    적금 = "적금"
    펀드 = "펀드"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    explanation = Column(String(255))
    ideal_rate = Column(Float)
    type = Column(Enum(ProductType))
    create_at = Column(DateTime, default=datetime.utcnow)
    modify_at = Column(DateTime, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
