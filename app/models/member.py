# from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Boolean, Enum, func, Date, DECIMAL
# from app.db.base import Base
# from app.schemas.member_schema import MemberRead 
# import enum


# class InvestTendency(enum.Enum):
#     안정형 = "안정형"
#     안정추구형 = "안정추구형"
#     위험중립형 = "위험중립형"
#     적극투자형 = "적극투자형"
#     공격투자형 = "공격투자형"


# class Member(Base):
#     __tablename__ = "members"

#     # 🔑 PK: DB는 BIGINT로 정의되었으며, autoincrement를 제거하여 수동 삽입된 ID를 지원합니다.
#     id = Column("user_id", BigInteger, primary_key=True, index=True) # 🚨 autoincrement 제거

#     # ✅ 이름 칼럼 (DB 칼럼명은 'name')
#     name = Column(String(255), nullable=False)

#     # ✅ 인증/부가 정보
#     email = Column(String(255), index=True, unique=True, nullable=False)
#     hashed_password = Column(String(255), nullable=False)
    
#     # 🚨 [복구된 칼럼] DB ALTER TABLE에 맞춰 추가
#     nickname = Column(String(50))              
#     is_superuser = Column(Boolean, default=False) 
    
#     # ✅ 신규 및 유지된 프로필 칼럼
#     job = Column(String(255))
#     gender = Column(Enum("M", "F", name="gender_enum"))
#     birth_date = Column(Date)

#     # ✅ 자산 및 투자 정보
#     initial_prop = Column(BigInteger)
#     currency = Column(BigInteger)
#     deposite_amount = Column(BigInteger)
#     saving_amount = Column(BigInteger)
#     fund_amount = Column(BigInteger)
#     invest_tendency = Column(String(50)) 

#     # ✅ 신규 추가된 대출/비율 정보
#     income_usage_ratio = Column(DECIMAL(5, 2)) 
#     is_loan_possible = Column(Boolean)
#     existing_loans = Column(Integer)
#     shortage_amount = Column(BigInteger)

#     # ✅ 나중에 채워질 희망 정보
#     hope_location = Column(String(255))
#     hope_price = Column(BigInteger)
#     hope_housing_type = Column(String(50))
    
#     created_at = Column(DateTime, server_default=func.now())

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Boolean,
    Enum,
    func,
)
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

    # PK: DB 컬럼명은 user_id, 파이썬에선 id 로 사용
    id = Column(
        "user_id",
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # 이름: DB 컬럼 name
    name = Column(String(255), nullable=False)

    # 생년월일: birth_date DATE
    birth_date = Column(Date, nullable=True)

    # 인증 정보
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # 직업 / 성별
    job = Column(String(30), nullable=True)
    gender = Column(
        Enum("M", "F", name="gender_enum"),
        nullable=True,
    )

    # 자산 및 금융 상태
    # 금액들은 BIGINT 로 잡아두면 안전 (DB가 int여도 MySQL에서 크게 문제 없음)
    initial_prop = Column(BigInteger, nullable=True)      # 초기 자산
    currency = Column(BigInteger, nullable=True)          # 현금 보유액
    deposite_amount = Column(BigInteger, nullable=True)   # 예금 금액
    saving_amount = Column(BigInteger, nullable=True)     # 적금 금액
    fund_amount = Column(BigInteger, nullable=True)       # 펀드 금액

    # 소득 사용 비율 / 대출 가능 여부
    income_usage_ratio = Column(String(10), nullable=True)      # VARCHAR(10)
    is_loan_possible = Column(Boolean, default=False)           # TINYINT(1)
    existing_loans = Column(Integer, nullable=True)             # 현재 대출 개수
    shortage_amount = Column(BigInteger, nullable=True)         # 부족 자금

    # 투자 성향 및 주택 희망 정보
    invest_tendency = Column(String(30), nullable=True)         # VARCHAR(30)
    hope_location = Column(String(80), nullable=True)
    hope_price = Column(Integer, nullable=True)
    hope_housing_type = Column(
        Enum(
            "아파트",
            "오피스텔",
            "단독다가구",
            "연립다세대",
            name="hope_housing_type_enum",
        ),
        nullable=True,
    )

    # 생성 시각
    created_at = Column(DateTime, server_default=func.now())