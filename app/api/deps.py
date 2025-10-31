# 각 api 실행을 위한 의존성(dependency)을 관리하는 파일
from app.db.session import SessionLocal
from collections.abc import Generator
from typing import Annotated
from sqlmodel import Session

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError
from dotenv import load_dotenv
from app.models.member import Member
from app.core import security
from app.schemas.token_schema import Token, TokenPayload
import os

load_dotenv()

BACKEND_URI = os.getenv("BACKEND_URI")

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{BACKEND_URI}/login/access-token"
)

def get_db() -> Generator[Session, None, None]:
    """
    db 조작을 위한 로컬 세션을 생성, 역할이 끝나면 종료하는 함수
    """
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()


# get_db 함수를 이용해 세션 의존성을 주입하는 타입 별칭(alias)
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> Member:
    """
    accessToken에서 사용자 정보를 뽑아내는 함수
    """
    try:
        payload = jwt.decode(
            token, security.JWT_SECRET_KEY, algorithms=[security.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    member = session.get(Member, token_data.sub)
    if not member:
        raise HTTPException(status_code=404, detail="User not found")
    return member


CurrentMember = Annotated[Member, Depends(get_current_user)]


def get_current_active_superuser(current_member: CurrentMember) -> Member:
    if not current_member.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_member