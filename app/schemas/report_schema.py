# backend/app/schemas/report_schema.py
from datetime import datetime
from typing import Any, Optional, Dict, List

from pydantic import BaseModel


class ReportBase(BaseModel):
    # 1) 소비 분석 결과
    consume_report: Optional[str] = None
    cluster_nickname: Optional[str] = None
    consume_analysis_summary: Optional[Dict[str, Any]] = None  # JSON_OBJECT
    
    spend_chart_json: Optional[Dict[str, Any]] = None

    # 2) 프로필 변동 사항
    change_analysis_report: Optional[str] = None
    change_raw_changes: Optional[List[str]] = None             # JSON_ARRAY

    # 3) 투자 수익 분석
    profit_analysis_report: Optional[str] = None
    net_profit: Optional[int] = None
    profit_rate: Optional[float] = None

    # 4) 정책 변동 사항
    policy_analysis_report: Optional[str] = None
    policy_changes: Optional[List[dict]] = None                # JSON 배열

    # 5) 최종 통합 요약
    threelines_summary: Optional[str] = None


class ReportRead(ReportBase):
    report_id: int
    user_id: int
    create_at: datetime        # ✅ 모델/DB랑 이름 맞추기

    class Config:
        orm_mode = True        # ✅ SQLAlchemy 객체 → 자동 변환
