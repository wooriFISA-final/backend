from typing import Any, Optional
# 🚨 [수정]: sqlmodel 대신 SQLAlchemy 표준 Session 및 select 임포트 사용
from sqlalchemy.orm import Session
from sqlalchemy import select 

from app.core.security import get_password_hash, verify_password
from app.models import Member
from app.schemas.member_schema import MemberCreate
import logging

logger = logging.getLogger(__name__)

def create_member(*, session: Session, member_create: MemberCreate) -> Member:
    """새로운 멤버 레코드를 생성하고 DB에 저장합니다."""
    # 🚨 [주의]: 이 함수는 SQLModel 스타일로 작성되어 있어 SQLAlchemy Session과 완벽 호환되지 않을 수 있지만,
    # 회원 생성 로직이므로 최대한 유지합니다.
    member_data = member_create.model_dump()
    hashed_pw = get_password_hash(member_data.pop("password"))

    # SQLAlchemy에서는 Model(**data) 방식이 일반적
    db_obj = Member(**member_data, hashed_password=hashed_pw)

    session.add(db_obj)
    # session.commit() 및 session.refresh(db_obj)는 SQLAlchemy/SQLModel에서 사용
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_member_by_email(*, session: Session, email: str) -> Member | None:
    """이메일을 기반으로 DB에서 사용자 레코드를 조회합니다."""
    
    try:
        statement = select(Member).where(Member.email == email)
        # 🚨 [핵심 수정]: session.exec -> session.execute로 변경
        session_user = session.execute(statement).scalars().first()
        return session_user
        
    except Exception as e:
        logger.error(f"🚨 DB 조회 오류 (get_member_by_email): 이메일={email}, 오류={e}")
        return None


def authenticate(*, session: Session, email: str, password: str) -> Member | None:
    """
    이메일과 비밀번호를 검증하여 사용자를 인증합니다.
    """
    # 1. 이메일로 사용자 조회
    db_user = get_member_by_email(session=session, email=email)
    
    if not db_user:
        return None

    # 2. 비밀번호 검증
    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user