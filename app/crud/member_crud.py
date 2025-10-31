from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Member
from app.schemas.member_schema import MemberCreate


def create_member(*, session: Session, member_create: MemberCreate) -> Member:
    member_data = member_create.model_dump()
    hashed_pw = get_password_hash(member_data.pop("password"))

    db_obj = Member(**member_data, hashed_password=hashed_pw)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_member_by_email(*, session: Session, email: str) -> Member | None:
    statement = select(Member).where(Member.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> Member | None:
    db_user = get_member_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
