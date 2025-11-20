# app/schemas/report.py
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class ReportBase(BaseModel):
    summarize: Optional[str] = None
    spend_chart_json: Optional[Any] = None
    spend_analysis_text: Optional[str] = None
    policy_changes: Optional[str] = None
    summary_3lines: Optional[str] = None
    user_info_changes: Optional[str] = None


class ReportRead(ReportBase):
    report_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True  # ✅ SQLAlchemy 객체 → 자동 변환
