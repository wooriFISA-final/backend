from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Boolean, Enum, func
from app.db.base import Base
from app.schemas.member_schema import MemberRead 
import enum


class InvestTendency(enum.Enum):
    안정형 = "안정형"
    안정추구형 = "안정추구형"
    위험중립형 = "위험중립형"
    적극투자형 = "적극투자형"
    공격투자형 = "공격투자형"


class Member(Base):
    __tablename__ = "members"

    # PK: DB 컬럼명은 user_id, 파이썬에선 id 로 사용
    id = Column("user_id", BigInteger, primary_key=True, index=True, autoincrement=True)

    # 이름: DB는 user_name, 파이썬에선 name
    name = Column("user_name", String(30), nullable=False)

    # 새로 추가한 인증/부가 정보
    nickname = Column(String(30))              # nickname
    email = Column(String(255), index=True)    # 나중에 UNIQUE/NOT NULL 가능
    hashed_password = Column(String(255))      # 비밀번호 해시
    is_superuser = Column(Boolean, default=False)

    # 기존 재무/주택 관련 컬럼들
    initial_prop = Column(Integer)
    hope_location = Column(String(80))
    hope_price = Column(Integer)
    hope_housing_type = Column(
        Enum("아파트", "오피스텔", "단독다가구", "연립다세대", name="hope_housing_type_enum"),
        nullable=True,
    )
    currency = Column(Integer)
    salary = Column(Integer)
    invest_tendency = Column(String(30))
    job = Column(String(30))
    age = Column(Integer)
    gender = Column(Enum("M", "F", name="gender_enum"))
    income_usage_ratio = Column(Integer)
    is_loan_possible = Column(Boolean, default=False)
    existing_loans = Column(Integer)
    shortage_amount = Column(BigInteger)
    created_at = Column(DateTime, server_default=func.now())
