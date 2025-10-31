from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class MyProduct(Base):
    __tablename__ = "my_products"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    current_value = Column(Integer)
    end_date = Column(DateTime)
    is_ended = Column(Boolean, default=False)

    plan = relationship("Plan", backref="my_products")
    product = relationship("Product", backref="my_products")
