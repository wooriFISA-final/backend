from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Float,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class MyProduct(Base):
    """
    사용자의 보유 금융상품(my_products) 테이블 ORM 모델

    실제 DB 스키마 (MySQL):

    - product_id BIGINT PK
    - user_id BIGINT FK → members.user_id
    - product_name VARCHAR(80)
    - product_type ENUM('예금','적금','펀드')
    - product_description VARCHAR(255)
    - current_value BIGINT
    - preferential_interest_rate DOUBLE
    - end_date DATETIME
    - created_at DATETIME
    - is_ended TINYINT(1)
    - payment_amount DECIMAL(15,2)
    - join_date DATETIME
    - principal_amount BIGINT
    """

    __tablename__ = "my_products"

    # PK: product_id
    product_id = Column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,  # AUTO_INCREMENT라면 True, 아니라면 빼도 됨
    )

    # 회원 FK: members.user_id
    user_id = Column(
        BigInteger,
        ForeignKey("members.user_id"),
        nullable=False,
        index=True,
    )

    # 상품 기본 정보
    product_name = Column(String(80), nullable=False)
    product_type = Column(
        Enum("예금", "적금", "펀드", name="product_type_enum"),
        nullable=False,
    )
    product_description = Column(String(255), nullable=True)

    # 금액 및 이율 정보
    current_value = Column(BigInteger, nullable=True)          # 현재 평가금액
    principal_amount = Column(BigInteger, nullable=True)       # 원금
    payment_amount = Column(Numeric(15, 2), nullable=True)     # 납입액(월/회차)
    preferential_interest_rate = Column(Float, nullable=True)  # 우대금리 (DOUBLE)

    # 기간/상태 정보
    join_date = Column(DateTime, nullable=True)                # 가입일
    end_date = Column(DateTime, nullable=True)                 # 만기일
    created_at = Column(DateTime, server_default=func.now())   # 생성일
    is_ended = Column(Boolean, default=False)                  # 종료 여부

    # 관계: Member ←→ MyProduct (1:N)
    member = relationship(
        "Member",
        backref="my_products",
        foreign_keys=[user_id],
    )
