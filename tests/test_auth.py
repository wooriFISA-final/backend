# tests/test_auth.py
import pytest
from datetime import timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.api.main import api_router
from app.core.security import create_access_token
from app.models.member import Member
from app.api.deps import get_current_user
from app.db.session import SessionLocal

client = TestClient(app)

@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_member(db_session):
    # 테스트용 회원 생성
    member = Member(email="test@example.com", hashed_password="hashedpw123", name="TestUser")
    db_session.add(member)
    db_session.commit()
    db_session.refresh(member)
    return member

def test_create_access_token():
    token = create_access_token(subject="123", expires_delta=timedelta(minutes=60))
    assert token is not None
    assert isinstance(token, str)

def test_get_current_user(db_session, test_member):
    # JWT 토큰 생성
    from app.core import security
    token = security.create_access_token(subject=test_member.id, expires_delta=timedelta(minutes=60))
    
    # 현재 유저 가져오기
    user = get_current_user(session=db_session, token=token)
    assert user.id == test_member.id
    assert user.email == "test@example.com"

def test_login_endpoint(db_session, test_member):
    response = client.post(
        "/login/access-token",
        data={"username": test_member.email, "password": "hashedpw123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_members_list_endpoint(db_session, test_member):
    # superuser 권한 부여
    test_member.is_superuser = True
    db_session.commit()

    token = create_access_token(subject=test_member.id, expires_delta=timedelta(minutes=60))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/members/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data
    assert any(u["id"] == test_member.id for u in data["data"])
