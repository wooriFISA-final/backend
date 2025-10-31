from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime


class PlanStatus(enum.Enum):
    진행중 = "진행중"
    종료 = "종료"


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    loan_amount = Column(Integer)
    target_self_capital = Column(Integer)
    target_price_fund = Column(Integer)
    target_price_saving = Column(Integer)
    target_loc = Column(String(255))
    target_build_type = Column(String(50))
    end_date = Column(DateTime)
    create_at = Column(DateTime, default=datetime.utcnow)
    plan_status = Column(Enum(PlanStatus))

    member = relationship("Member", backref="plans")
