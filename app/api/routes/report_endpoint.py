# backend/app/api/routes/report_endpoint.py
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

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
    current_member: CurrentMember,
):
    stmt = (
        select(Report)
        .where(Report.user_id == current_member.id)  # 혹은 current_member.user_id
        .order_by(Report.create_at.desc())           # ✅ create_at 이름 맞추기
    )
    result = db.execute(stmt)
    reports = result.scalars().all()
    return reports


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
