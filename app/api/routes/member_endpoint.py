import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from crud import member_crud
from api.deps import (
    CurrentMember,
    SessionDep,
    get_current_active_superuser
)
from core.security import get_password_hash, verify_password
from models import Member
from schemas.member_schema import MembersPublic, MemberPublic, MemberCreate, MemberRegister

router = APIRouter(prefix="/members", tags=["members"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MemberPublic,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    유저 리스트를 검색하는 함수
    기본적으로 100명 까지 검색
    """

    count_statement = select(func.count()).select_from(Member)
    count = session.exec(count_statement).one()

    statement = select(Member).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return MembersPublic(data=users, count=count)


# @router.post(
#     "/", dependencies=[Depends(get_current_active_superuser)], response_model=MemberPublic
# )
# def create_user(*, session: SessionDep, member_in: MemberCreate) -> Any:
#     """
#     새로운 유저 생성 (e-mail 사용버젼)
#     """
#     member = member_crud.get_member_by_email(session=session, email=member_in.email)
#     if member:
#         raise HTTPException(
#             status_code=400,
#             detail="해당 e-mail로 가입된 이용자가 이미 있습니다.",
#         )

#     member = member_crud.create_user(session=session, user_create=member_in)
#     if settings.emails_enabled and member_in.email:
#         email_data = generate_new_account_email(
#             email_to=member_in.email, username=member_in.email, password=member_in.password
#         )
#         send_email(
#             email_to=member_in.email,
#             subject=email_data.subject,
#             html_content=email_data.html_content,
#         )
#     return user


@router.post("/signup", response_model=MemberPublic)
def register_user(session: SessionDep, user_in: MemberRegister) -> Any:
    """
    슈퍼유저 로그인 없이 회원가입 하게 하기
    """
    member = member_crud.get_member_by_email(session=session, email=user_in.email)
    if member:
        raise HTTPException(
            status_code=400,
            detail="해당 e-mail로 가입된 이용자가 이미 있습니다.",
        )
    member_create = MemberCreate.model_validate(user_in)
    member = member_crud.create_member(session=session, user_create=member_create)
    return member


@router.get("/{member_id}", response_model=MemberPublic)
def read_user_by_id(
    member_id: uuid.UUID, session: SessionDep, current_member: CurrentMember
) -> Any:
    """
    멤버 ID로 특정 멤버 조회하기
    """
    member = session.get(Member, member_id)
    if member == current_member:
        return member
    if not current_member.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="관리자를 조회하기 위한 권한이 없습니다.",
        )
    return member

