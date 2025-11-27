from datetime import timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm # 🚨 이 표준만 사용하도록 복원

from app import crud
from app.api.deps import CurrentMember, SessionDep
from app.core import security
from app.schemas.token_schema import Token
from app.crud import member_crud
from app.schemas.member_schema import MemberPublic 
from app.crud import member_crud
# 🚨 주의: EmailPassword 스키마 임포트 및 정의는 여기서 제거합니다.

router = APIRouter(tags=["login"])
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, 
    # 🚨 [핵심 수정]: Union 및 복잡한 Boday 로직 제거, 표준 OAuth2로 복원
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()] 
) -> Token:
    """
    OAuth2 와 호환 가능한 token login,
    향후 request 처리를 위한 access token을 발급한다
    """
    
    # 클라이언트가 보낸 username을 DB의 email 칼럼에 매핑합니다.
    member = member_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not member:
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 정확하지 않습니다.")
    
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
