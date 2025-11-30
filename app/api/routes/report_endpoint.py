# backend/app/api/routes/report_endpoint.py
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from datetime import datetime

from app.api.deps import SessionDep, CurrentMember
from app.models import Report
from app.schemas.report_schema import ReportRead

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/", response_model=List[ReportRead])
def list_reports(
    db: SessionDep,
    # current_member: CurrentMember,  # 🚨 임시로 비활성화
):
    # 🚨 1. 요청 도착 및 함수 진입 확인
    print("\n========================================================")
    print(f"[DEBUG:R-LIST] 1. list_reports 요청 도착: {datetime.now().strftime('%H:%M:%S')}") 
    # print(f"[DEBUG:R-LIST] 2. 인증 완료. 사용자 ID: {current_member.id}")  # 🚨 임시로 비활성화
    print("========================================================")
    
    try:
        stmt = (
            select(Report)
            # .where(Report.user_id == current_member.id)  # 🚨 임시로 비활성화 - 모든 리포트 조회
            .order_by(Report.create_at.desc())
        )
        
        # 🚨 3. DB 쿼리 실행 직전 확인 (여기서 멈추면 DB 연결 지연)
        print(f"[DEBUG:R-LIST] 3. DB 쿼리 실행 직전 시각: {datetime.now().strftime('%H:%M:%S')}")
        
        # ⚠️ 실제 DB 쿼리 실행 (병목 예상 지점)
        result = db.execute(stmt)
        reports = result.scalars().all()
        
        # 🚨 4. DB 쿼리 완료 후 데이터 개수 확인
        print(f"[DEBUG:R-LIST] 4. DB 조회 완료. 리포트 개수: {len(reports)} 개. 시각: {datetime.now().strftime('%H:%M:%S')}")
        
        # 🚨 5. 응답 직전 확인
        print(f"[DEBUG:R-LIST] 5. 최종 응답 직전.")
        return reports
    
    except Exception as e:
        # 🚨 6. 예외 발생 시 상세 내용 확인
        print(f"[DEBUG:R-LIST] 6. 함수 처리 중 예외 발생: {type(e).__name__}: {e}")
        # DB 연결 오류 등은 여기서 500 에러를 발생시킬 수 있습니다.
        raise HTTPException(status_code=500, detail="서버 내부 처리 오류 발생")


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
