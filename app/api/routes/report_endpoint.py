# backend/app/api/routes/report_endpoint.py

from typing import List, Union, Dict, Any, Optional
from decimal import Decimal
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from datetime import datetime

# 🚨 실제 경로에 맞게 임포트 경로를 수정해야 합니다. (예시 경로 유지)
from app.api.deps import SessionDep, CurrentMember # SessionDep은 Session = Annotated[Session, Depends(get_db)] 와 같은 형태로 가정
from app.models import Report # Report 모델 임포트 가정
from app.schemas.report_schema import ReportRead # ReportRead 스키마 임포트 가정

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


# 🚨 [신규 함수]: DB 데이터를 Pydantic에 맞게 정리하는 유틸리티
def _clean_report_data(report_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    DB에서 가져온 딕셔너리를 Pydantic 스키마에 맞게 정규화합니다.
    - {} 또는 빈 JSON 문자열을 None으로 변환하여 Optional 필드의 유효성 검사를 통과시킵니다.
    - Decimal 객체를 float/int로 변환합니다.
    """
    
    # 1. JSON 필드 정규화 (빈 객체/빈 문자열 -> None)
    json_fields = [
        "consume_analysis_summary", 
        "spend_chart_json", 
        "change_raw_changes", 
        "policy_changes", # 유효성 검사 오류의 주요 원인
        "trend_chart_json", 
        "fund_comparison_json"
    ]
    
    for key in json_fields:
        value = report_dict.get(key)
        
        # 빈 딕셔너리 {} 또는 None은 그대로 None으로 처리
        if value == {} or value is None:
            report_dict[key] = None
        # 빈 JSON 문자열 '[]' 또는 '{}' 또는 'null' 문자열도 None으로 처리
        elif isinstance(value, str) and value.strip() in ('[]', '{}', 'null', ''):
            report_dict[key] = None
        # 데이터가 딕셔너리 형태인데, 핵심 리스트(changes/policy_changes)를 포함하는 경우 처리 (정규화)
        elif isinstance(value, dict):
            # 오류 로그에서 확인된 딕셔너리 형태를 처리 (예: {'changes': [...]} 또는 {'message': ...})
            
            # 여기서 리스트를 추출하는 구체적인 로직을 추가할 수 있으나,
            # 스키마에서 Dict[str, Any]를 허용한 경우 이 단계는 생략하고 Pydantic에 맡기는 것이 더 안전할 수 있습니다.
            # 하지만 빈 딕셔너리만 None 처리하고, 실제 데이터가 있는 딕셔너리는 유지하여 Pydantic이 처리하도록 합니다.
            pass
            
    # 2. Decimal 객체 Float/Int로 변환
    for key, value in report_dict.items():
        if isinstance(value, Decimal):
            # net_profit은 정수, profit_rate는 실수라고 가정하고 처리
            if key == "net_profit":
                 report_dict[key] = int(value)
            elif key == "profit_rate":
                report_dict[key] = float(value)
            else:
                # 다른 Decimal 필드도 float으로 변환하여 JSON 직렬화 오류 방지
                report_dict[key] = float(value)
        elif isinstance(value, (int, float)):
             # 숫자 값은 그대로 유지
             report_dict[key] = value

    return report_dict


@router.get("/", response_model=List[ReportRead])
def list_reports(
    db: SessionDep,
    # current_member: CurrentMember, 
):
    print("\n========================================================")
    print(f"[DEBUG:R-LIST] 1. list_reports 요청 도착: {datetime.now().strftime('%H:%M:%S')}") 
    print("========================================================")
    
    try:
        # 🚨 테스트 환경에서는 user_id 필터링을 주석 처리하고 전체 리포트를 조회
        stmt = (
            select(Report)
            # .where(Report.user_id == current_member.id) 
            .order_by(Report.create_at.desc())
        )
        
        print(f"[DEBUG:R-LIST] 3. DB 쿼리 실행 직전 시각: {datetime.now().strftime('%H:%M:%S')}")
        
        result = db.execute(stmt)
        reports = result.scalars().all()
        
        print(f"[DEBUG:R-LIST] 4. DB 조회 완료. 리포트 개수: {len(reports)} 개. 시각: {datetime.now().strftime('%H:%M:%S')}")
        
        response_data = []
        for report in reports:
            # SQLAlchemy 객체를 dict로 변환
            report_dict = {c.name: getattr(report, c.name) for c in report.__table__.columns}
            
            # 🚨 [필수 수정]: DB에서 바로 가져온 report_dict를 먼저 클리닝하여 유효성 검사 대비
            report_dict = _clean_report_data(report_dict)

            # 리포트 생성 월 (YYYY-MM) 추출
            report_month_dt = report.create_at if isinstance(report.create_at, datetime) else datetime.strptime(report.create_at.strftime("%Y-%m-%d"), "%Y-%m-%d")
            report_month_str = report_month_dt.strftime("%Y-%m")
            
            # ------------------------------------------------------------------------------------------------------
            # 1) 월별 자산 추이 데이터 조회 (monthly_simulation_report)
            # ------------------------------------------------------------------------------------------------------
            try:
                sim_query = text("""
                    SELECT year_and_month, deposit_balance, savings_balance, fund_balance, total_asset 
                    FROM monthly_simulation_report 
                    WHERE user_id = :uid 
                      AND year_and_month <= :report_month
                    ORDER BY year_and_month DESC 
                    LIMIT 12
                """)
                sim_result = db.execute(sim_query, {"uid": report.user_id, "report_month": report_month_str}).fetchall()
                
                trend_data = []
                for row in reversed(sim_result):
                    # 🚨 Decimal/None 처리 추가 및 정수 변환
                    trend_data.append({
                        "month": row.year_and_month,
                        "deposit_balance": int(row.deposit_balance) if row.deposit_balance is not None else 0,
                        "savings_balance": int(row.savings_balance) if row.savings_balance is not None else 0,
                        "fund_balance": int(row.fund_balance) if row.fund_balance is not None else 0,
                        "total_asset": int(row.total_asset) if row.total_asset is not None else 0
                    })
                
                # 🚨 Pydantic 모델에 맞게 객체 자체로 저장
                report_dict["trend_chart_json"] = trend_data 
            except Exception as e:
                print(f"⚠️ 그래프1 데이터 조회 실패: {e}")
                report_dict["trend_chart_json"] = [] # 빈 리스트로 설정

            # ------------------------------------------------------------------------------------------------------
            # 2) 펀드 상품별 수익률 비교 데이터 조회 (monthly_fund_portfolio_snapshot)
            # ------------------------------------------------------------------------------------------------------
            try:
                latest_month_query = text("""
                    SELECT MAX(year_and_month) 
                    FROM monthly_fund_portfolio_snapshot 
                    WHERE user_id = :uid 
                      AND year_and_month <= :report_month
                """)
                max_month = db.execute(latest_month_query, {"uid": report.user_id, "report_month": report_month_str}).scalar()
                
                fund_data = []
                if max_month:
                    fund_query = text("""
                        SELECT fund_product_name, invested_amount, eval_amount 
                        FROM monthly_fund_portfolio_snapshot 
                        WHERE user_id = :uid AND year_and_month = :month
                    """)
                    fund_result = db.execute(fund_query, {"uid": report.user_id, "month": max_month}).fetchall()
                    
                    for row in fund_result:
                        invested = float(row.invested_amount) if row.invested_amount is not None else 0
                        eval_amt = float(row.eval_amount) if row.eval_amount is not None else 0
                        
                        return_rate = ((eval_amt - invested) / invested * 100) if invested > 0 else 0
                        
                        fund_data.append({
                            "name": row.fund_product_name,
                            "return_rate": round(return_rate, 2)
                        })
                
                # 🚨 Pydantic 모델에 맞게 객체 자체로 저장
                report_dict["fund_comparison_json"] = fund_data 
            except Exception as e:
                print(f"⚠️ 그래프2 데이터 조회 실패: {e}")
                report_dict["fund_comparison_json"] = [] # 빈 리스트로 설정
                
            response_data.append(report_dict)
        
        print(f"[DEBUG:R-LIST] 5. 최종 응답 직전.")
        
        # 🚨 [최종 반환]: 클리닝된 딕셔너리 리스트를 반환하여 FastAPI가 Pydantic 모델 유효성 검사를 수행하도록 합니다.
        return response_data
    
    except Exception as e:
        print(f"[DEBUG:R-LIST] 6. 함수 처리 중 예외 발생: {type(e).__name__}: {e}")
        # 🚨 오류 발생 시 500 에러 대신 상세 정보를 포함하여 반환 (디버깅 용이)
        raise HTTPException(status_code=500, detail=f"서버 내부 처리 오류 발생: {type(e).__name__}: {str(e)}")


@router.get("/{report_id}", response_model=ReportRead)
def get_my_report(
    report_id: int,
    db: SessionDep,
    current_member: CurrentMember,
):
    stmt = (
        select(Report)
        .where(
            Report.report_id == report_id,
            Report.user_id == current_member.id,
        )
    )
    result = db.execute(stmt)
    report = result.scalars().first()

    if not report:
        raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")

    return report