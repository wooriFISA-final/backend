# app/api/routes/report_endpoint.py
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select  # ✅ sqlmodel 말고 sqlalchemy 쪽 select 사용

from app.api.deps import SessionDep  # 테스트 용이라 CurrentMember는 잠깐 제거
from app.models import Report
from app.schemas.report_schema import ReportRead

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/", response_model=List[ReportRead])
def list_reports(
    db: SessionDep,
    # current_member: CurrentMember,   # ⬅ 나중에 인증 붙일 때 다시 사용
):
    """
    (테스트용) 모든 리포트 목록 조회
    - 나중에는 current_member.user_id 기준으로 필터링할 예정
    """
    stmt = select(Report).where(Report.created_at)
    result = db.execute(stmt)           # ✅ SQLAlchemy Session에는 execute 사용
    reports = result.scalars().all()    # ✅ Report 객체 리스트로 변환

    return reports


@router.get("/{report_id}", response_model=ReportRead)
def get_my_report(
    report_id: int,
    db: SessionDep,
    # current_member: CurrentMember,  # ⬅ 나중에 인증 붙일 때 다시 사용
):
    """
    (테스트용) 단일 리포트 상세 조회
    - 나중에는 Report.user_id == current_member.user_id 조건도 추가할 예정
    """
    stmt = select(Report).where(
        Report.report_id == report_id,
        # Report.user_id == current_member.user_id,  # ⬅ 인증 붙일 때 같이 사용
    )
    result = db.execute(stmt)
    report = result.scalars().first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report
