# app/models/report.py
from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    # MySQL: report_id BIGINT PRIMARY KEY
    report_id = Column(BigInteger, primary_key=True, index=True)

    # MySQL: user_id BIGINT NOT NULL REFERENCES members(user_id)
    user_id = Column(
        BigInteger,
        ForeignKey("members.id"),   # ⚠ Member.user_id 이 있다고 가정
        nullable=False,
        index=True,
    )

    # MySQL 컬럼 이름이 create_at 이고,
    # 파이썬 코드에서는 created_at 으로 쓰고 싶다면 이렇게 매핑:
    created_at = Column("created_at", DateTime, default=datetime.utcnow)

    # 요약 텍스트
    summarize = Column(Text, nullable=True)

    # 추가 리포트 정보들 (NULL 허용)
    spend_chart_json = Column(JSON, nullable=True)
    spend_analysis_text = Column(Text, nullable=True)
    policy_changes = Column(Text, nullable=True)
    summary_3lines = Column(String(512), nullable=True)
    user_info_changes = Column(Text, nullable=True)

    # Member와의 관계
    member = relationship("Member", backref="reports")
