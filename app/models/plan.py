from datetime import datetime
import enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class PlanStatus(enum.Enum):
    진행중 = "진행중"
    종료 = "종료"


class Plan(Base):
    __tablename__ = "plans"

    # PK: DB 컬럼명 plan_id, 파이썬에서는 id 로 사용
    id = Column(
        "plan_id",
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # FK: plans.user_id → members.user_id
    user_id = Column(
        BigInteger,
        ForeignKey("members.user_id"),
        nullable=False,
        index=True,
    )

    # 금액 관련 컬럼들 (BIGINT)
    loan_amount = Column(BigInteger, nullable=True)
    target_self_capital = Column(BigInteger, nullable=True)
    target_price_fund = Column(BigInteger, nullable=True)
    target_price_saving = Column(BigInteger, nullable=True)
    target_price_deposit = Column(BigInteger, nullable=True)

    # 목표 주택 정보
    target_loc = Column(String(80), nullable=True)
    target_build_type = Column(
        Enum(
            "아파트",
            "오피스텔",
            "단독다가구",
            "연립다세대",
            name="target_build_type_enum",
        ),
        nullable=True,
    )

    # 기간/상태
    end_date = Column(DateTime, nullable=True)
    create_at = Column(DateTime, server_default=func.now())  # DB 컬럼명과 동일
    plan_status = Column(
        Enum(PlanStatus, name="plan_status_enum"),
        nullable=True,
    )

    # 연결된 상품 / 요약 리포트
    product_id = Column(Integer, nullable=True)          # 필요 시 FK로 확장 가능
    summary_report = Column(Text, nullable=True)         # MEDIUMTEXT 매핑

    # Member 관계 (1 : N)
    member = relationship(
        "Member",
        backref="plans",
        foreign_keys=[user_id],
    )
