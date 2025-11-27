from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Boolean, Enum, func, Date, DECIMAL
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

    # 🔑 PK: DB는 BIGINT로 정의되었으며, autoincrement를 제거하여 수동 삽입된 ID를 지원합니다.
    id = Column("user_id", BigInteger, primary_key=True, index=True) # 🚨 autoincrement 제거

    # ✅ 이름 칼럼 (DB 칼럼명은 'name')
    name = Column(String(255), nullable=False)

    # ✅ 인증/부가 정보
    email = Column(String(255), index=True, unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # 🚨 [복구된 칼럼] DB ALTER TABLE에 맞춰 추가
    nickname = Column(String(50))              
    is_superuser = Column(Boolean, default=False) 
    
    # ✅ 신규 및 유지된 프로필 칼럼
    job = Column(String(255))
    gender = Column(Enum("M", "F", name="gender_enum"))
    birth_date = Column(Date)

    # ✅ 자산 및 투자 정보
    initial_prop = Column(BigInteger)
    currency = Column(BigInteger)
    deposite_amount = Column(BigInteger)
    saving_amount = Column(BigInteger)
    fund_amount = Column(BigInteger)
    invest_tendency = Column(String(50)) 

    # ✅ 신규 추가된 대출/비율 정보
    income_usage_ratio = Column(DECIMAL(5, 2)) 
    is_loan_possible = Column(Boolean)
    existing_loans = Column(Integer)
    shortage_amount = Column(BigInteger)

    # ✅ 나중에 채워질 희망 정보
    hope_location = Column(String(255))
    hope_price = Column(BigInteger)
    hope_housing_type = Column(String(50))
    
    created_at = Column(DateTime, server_default=func.now())