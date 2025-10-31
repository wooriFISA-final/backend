from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from deps import CurrentMember, SessionDep, get_current_active_superuser
from core import security
from core.security import get_password_hash
from schemas.global_schema import Message
from schemas.token_schema import Token
from schemas.member_schema import MemberPublic
from crud import member_crud

router = APIRouter(tags=["login"])
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1시간 * 24 * 7 -> 총 7일


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    member = member_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not member:
        raise HTTPException(status_code=400, detail="e-mail 또는 비밀번호가 정확하지 않습니다.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            member.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=MemberPublic)
def test_token(current_member: CurrentMember) -> Any:
    """
    access token 을 테스트하는 api
    """
    return current_member
