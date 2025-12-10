# 🗄️ WooriZip Backend - FastAPI Backend Server

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.120+-green?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLModel-0.0.27+-orange?logo=sqlalchemy&logoColor=white" alt="SQLModel">
  <img src="https://img.shields.io/badge/MySQL-8.0+-blue?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/JWT-Auth-red?logo=jsonwebtokens&logoColor=white" alt="JWT">
</p>

<p align="center">
  FastAPI + SQLModel 기반의 RESTful API 백엔드 서버로<br/>
  <strong>사용자 인증, 재무 계획 관리, 리포트 저장</strong> 기능을 제공합니다.
</p>

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Configuration](#%EF%B8%8F-configuration)
- [API Reference](#-api-reference)
- [Database Models](#-database-models)
- [Project Structure](#-project-structure)
- [Docker Deployment](#-docker-deployment)

---

## ✨ Features

### 🎯 주요 기능
- **사용자 인증** - JWT 기반 로그인/회원가입
- **회원 관리** - 사용자 정보 CRUD
- **재무 계획** - Plan 저장 및 조회
- **리포트 관리** - 재무 리포트 저장/조회
- **상품 관리** - 금융 상품 정보 관리

### 🔧 기술적 특징
- 🔐 **JWT 인증** - Access Token 기반 인증
- 📊 **SQLModel ORM** - Pydantic + SQLAlchemy 통합
- 🔄 **Alembic Migration** - 데이터베이스 마이그레이션
- 🌐 **CORS 지원** - 프론트엔드 연동
- 📝 **Swagger UI** - 자동 API 문서화

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| **Framework** | FastAPI 0.120+ |
| **Language** | Python 3.11 |
| **ORM** | SQLModel, SQLAlchemy 2.0 |
| **Database** | MySQL 8.0 (AWS RDS) |
| **Migration** | Alembic |
| **Auth** | JWT (python-jose, PyJWT) |
| **Security** | bcrypt, passlib |
| **Package Manager** | uv |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MySQL 8.0+ (또는 AWS RDS)
- uv (권장) 또는 pip

### 30초 시작하기

```bash
# 1. 저장소 클론
git clone https://github.com/your-org/woorizip-backend.git
cd backend

# 2. 환경 변수 설정
cp .env.sample .env
# .env 파일에서 DB 연결 정보 등 설정

# 3. 의존성 설치
pip install uv
uv pip install --system .

# 4. 데이터베이스 마이그레이션
alembic upgrade head

# 5. 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

서버가 시작되면:
- 📖 Swagger UI: `http://localhost:8000/docs`
- 📖 ReDoc: `http://localhost:8000/redoc`

---

## ⚙️ Configuration

### 환경 변수 (.env)

```bash
# ============================================
# Database Configuration
# ============================================
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=woorizip

# ============================================
# JWT Settings
# ============================================
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# ============================================
# Server Settings
# ============================================
BACKEND_URI=localhost

# ============================================
# CORS Settings (쉼표로 구분)
# ============================================
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://woorizip.info
```

### 환경별 설정

| 환경 | DB_HOST | BACKEND_URI | Port |
|------|---------|-------------|------|
| **개발** | `localhost` | `localhost` | 8000 |
| **프로덕션** | RDS Endpoint | EC2 Private IP | 8000 |

---

## 📖 API Reference

### Base URL
```
http://localhost:8000
```

### 🔐 인증 API

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/login` | 로그인 (JWT 토큰 발급) |
| `POST` | `/api/signup` | 회원가입 |
| `GET` | `/api/me` | 현재 사용자 정보 |

### 👤 회원 API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/members` | 회원 목록 조회 |
| `GET` | `/api/members/{id}` | 회원 상세 조회 |
| `PUT` | `/api/members/{id}` | 회원 정보 수정 |
| `DELETE` | `/api/members/{id}` | 회원 삭제 |

### 📝 리포트 API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/reports` | 리포트 목록 조회 |
| `GET` | `/api/reports/{id}` | 리포트 상세 조회 |
| `POST` | `/api/reports` | 리포트 생성 |
| `PUT` | `/api/reports/{id}` | 리포트 수정 |
| `DELETE` | `/api/reports/{id}` | 리포트 삭제 |

### 📊 계획 API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/plans` | 재무 계획 목록 |
| `GET` | `/api/plans/{id}` | 계획 상세 조회 |
| `POST` | `/api/plans` | 계획 저장 |

---

## 🗃️ Database Models

### Member (회원)
```python
class Member:
    id: int                 # PK
    email: str              # 이메일 (Unique)
    password: str           # 해시된 비밀번호
    name: str               # 이름
    created_at: datetime    # 가입일
```

### Plan (재무 계획)
```python
class Plan:
    id: int                 # PK
    member_id: int          # FK -> Member
    target_amount: int      # 목표 금액
    monthly_saving: int     # 월 저축액
    period_months: int      # 기간 (월)
    created_at: datetime    # 생성일
```

### Report (리포트)
```python
class Report:
    id: int                 # PK
    member_id: int          # FK -> Member
    plan_id: int            # FK -> Plan
    content: str            # 리포트 내용
    created_at: datetime    # 생성일
```

### Product (금융 상품)
```python
class Product:
    id: int                 # PK
    name: str               # 상품명
    type: str               # 상품 유형 (예금/적금/대출)
    interest_rate: float    # 금리
```

---

## 📁 Project Structure

```
backend/
├── app/                        # 🚀 애플리케이션
│   ├── main.py                 # FastAPI 앱 엔트리포인트
│   │
│   ├── api/                    # API 레이어
│   │   ├── main.py             # 라우터 통합
│   │   ├── deps.py             # 의존성 (인증 등)
│   │   └── routes/             # 엔드포인트
│   │       ├── login_endpoint.py   # 로그인/인증
│   │       ├── member_endpoint.py  # 회원 관리
│   │       └── report_endpoint.py  # 리포트 관리
│   │
│   ├── models/                 # 📊 데이터 모델
│   │   ├── member.py           # 회원 모델
│   │   ├── plan.py             # 계획 모델
│   │   ├── report.py           # 리포트 모델
│   │   ├── product.py          # 상품 모델
│   │   ├── house.py            # 주택 모델
│   │   ├── policy.py           # 정책 모델
│   │   ├── my_product.py       # 나의 상품
│   │   └── chat_history.py     # 채팅 히스토리
│   │
│   ├── schemas/                # 📝 Pydantic 스키마
│   │   ├── member.py           # 회원 스키마
│   │   ├── plan.py             # 계획 스키마
│   │   └── report.py           # 리포트 스키마
│   │
│   ├── crud/                   # 🔄 CRUD 로직
│   │   ├── member_crud.py      # 회원 CRUD
│   │   └── report_crud.py      # 리포트 CRUD
│   │
│   ├── core/                   # ⚙️ 핵심 설정
│   │   ├── config.py           # 설정 관리
│   │   └── security.py         # 보안 (JWT, 해싱)
│   │
│   ├── db/                     # 🗄️ 데이터베이스
│   │   ├── session.py          # DB 세션
│   │   └── base.py             # Base 모델
│   │
│   └── alembic/                # 🔄 마이그레이션
│       ├── versions/           # 마이그레이션 버전
│       └── env.py              # Alembic 설정
│
├── alembic.ini                 # Alembic 설정 파일
├── dockerfile                  # Docker 빌드
├── requirements.txt            # 의존성 목록
├── pyproject.toml              # 프로젝트 설정
├── .env.sample                 # 환경 변수 템플릿
└── DOCKER_DEPLOYMENT.md        # Docker 배포 가이드
```

---

## 🐳 Docker Deployment

### 빠른 배포

```bash
# 환경 변수 설정
cp .env.sample .env
# .env 파일 수정

# Docker 이미지 빌드
docker build -t woorizip-backend:latest .

# 컨테이너 실행
docker run -d \
  --name backend \
  -p 8000:8000 \
  --env-file .env \
  woorizip-backend:latest
```

### 로그 확인

```bash
docker logs -f backend
```

---

## 🔄 Database Migration

### Alembic 명령어

```bash
# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Add new column"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1

# 현재 버전 확인
alembic current
```

---

## 🧪 Testing

```bash
# 테스트 실행
pytest

# 특정 테스트 실행
pytest tests/test_member.py -v

# 커버리지 포함
pytest --cov=app
```

---

## 🔒 Security

- ✅ JWT 토큰 기반 인증
- ✅ 비밀번호 bcrypt 해싱
- ✅ CORS 설정으로 허용된 도메인만 접근
- ✅ 환경 변수로 민감한 정보 관리
- ✅ SQLAlchemy 파라미터 바인딩 (SQL Injection 방지)

---

<p align="center">
  Made by WooriFisa Team 6
</p>
