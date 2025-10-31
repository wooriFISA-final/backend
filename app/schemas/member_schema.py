from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr


# 공통 속성
class MemberBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_superuser: bool = False
    name: str | None = Field(default=None, max_length=255)


# 멤버 생성
class MemberCreate(MemberBase):
    password: str = Field(min_length=8, max_length=128)


class MemberRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=3, max_length=128)
    name: str | None = Field(default=None, max_length=255)


# 멤버 id 포함한 기본정보
class MemberPublic(MemberBase):
    id: int


# 멤버 리스트
class MembersPublic(SQLModel):
    data: list[MemberPublic]
    count: int


