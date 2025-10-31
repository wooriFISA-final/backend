from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.db.base import Base
import enum


class InvestTendency(enum.Enum):
    안정형 = "안정형"
    안정추구형 = "안정추구형"
    위험중립형 = "위험중립형"
    적극투자형 = "적극투자형"
    공격투자형 = "공격투자형"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    nickname = Column(String(255))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    initial_prop = Column(Integer)  # 초기 자산
    hope_loc = Column(String(255))
    hope_price = Column(Integer)
    hope_build_type = Column(String(50))
    currency = Column(String(20))
    salary = Column(Integer)
    invest_tendency = Column(Enum(InvestTendency))
    is_superuser = Column(Boolean, default=False)
