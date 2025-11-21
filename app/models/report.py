# backend/app/models/report.py
from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    Text,
    String,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.dialects.mysql import JSON  # ✅ MySQL JSON 타입
from sqlalchemy.orm import relationship

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("members.user_id"), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 1) 소비 분석 결과
    consume_report = Column(Text)               # TEXT
    cluster_nickname = Column(String(100))      # VARCHAR(100)
    consume_analysis_summary = Column(JSON)     # JSON
    
    spend_chart_json = Column(JSON)

    # 2) 프로필 변동 사항
    change_analysis_report = Column(Text)       # TEXT
    change_raw_changes = Column(JSON)          # JSON 배열

    # 3) 투자 수익 분석
    profit_analysis_report = Column(Text)       # TEXT
    net_profit = Column(BigInteger)            # BIGINT
    profit_rate = Column(DECIMAL(10, 4))       # DECIMAL(10,4)

    # 4) 정책 변동 사항
    policy_analysis_report = Column(Text)       # TEXT
    policy_changes = Column(JSON)              # JSON

    # 5) 최종 통합 요약
    threelines_summary = Column(Text)          # TEXT

    # 관계 (선택)
    member = relationship("Member", backref="reports")
