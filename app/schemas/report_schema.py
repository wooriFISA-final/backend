# backend/app/schemas/report_schema.py

from datetime import datetime
from typing import Any, Optional, Dict, List
from pydantic import BaseModel, ConfigDict # ConfigDict 임포트 필요 (Pydantic V2 대응)

# 🚨 ChartDataArray 스키마 추가
class ChartDataArray(BaseModel):
    category: str
    amount: float
    
    # Pydantic V2 대응
    model_config = ConfigDict(from_attributes=True) 

# ------------------------------------------------------------------

class ReportBase(BaseModel):
    # 1) 소비 분석 결과
    consume_report: Optional[str] = None
    cluster_nickname: Optional[str] = None
    # 🚨 문자열도 허용 (DB에 문자열로 저장된 경우 대응)
    consume_analysis_summary: Optional[Dict[str, Any] | str] = None
    
    # 🚨 문자열도 허용 (DB에 문자열로 저장된 경우 대응)
    # spend_chart_json: Optional[List[ChartDataArray] | str] = None
    spend_chart_json: Optional[List[ChartDataArray]] = None

    # 2) 프로필 변동 사항
    change_analysis_report: Optional[str] = None
    change_raw_changes: Optional[List[str] | str] = None

    # 3) 투자 수익 분석
    profit_analysis_report: Optional[str] = None
    net_profit: Optional[int] = None
    profit_rate: Optional[float] = None
    trend_chart_json: Optional[List[Dict[str, Any]] | str] = None  # 🆕 월별 투자 수익률 추이
    fund_comparison_json: Optional[List[Dict[str, Any]] | str] = None  # 🆕 펀드 상품별 손익

    # 4) 정책 변동 사항
    policy_analysis_report: Optional[str] = None
    policy_changes: Optional[List[Any] | Dict[str, Any] | str] = None
    threelines_summary: Optional[str] = None


class ReportRead(ReportBase):
    report_id: int
    user_id: int
    create_at: datetime

    class Config:
        orm_mode = True        # 🚨 (Pydantic V1 스타일)
        
    # 🚨 Pydantic V2에서는 아래를 사용합니다 (Config: orm_mode 대신)
    # model_config = ConfigDict(from_attributes=True)