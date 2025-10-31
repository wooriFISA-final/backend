from sqlalchemy import Column, Integer, String, Enum
from db.base import Base
import enum


class HouseType(enum.Enum):
    아파트 = "아파트"
    빌라 = "빌라"
    오피스텔 = "오피스텔"


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    sigungu_code = Column(String(20))
    price = Column(Integer)
    type = Column(Enum(HouseType))
