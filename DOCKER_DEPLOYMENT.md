# 🚀 Backend Docker 배포 가이드 (완벽 가이드)

## 📋 개요

Backend FastAPI 애플리케이션을 Docker로 컨테이너화하여 EC2 인스턴스에 배포하는 전체 과정입니다.

---

## 🏗️ 현재 구조

```
Backend 인스턴스 (Private Subnet)
  - MCP 서버 (포트: ?)
  - Backend 서버 (포트: 8000) ← 이것을 배포
  - Dummy API 서버 (포트: ?)
  - Private IP: 10.0.2.10 (예시)
```

---

## 📦 Step 1: 환경 변수 설정

### 1-1. `.env.production` 파일 생성

Backend 폴더에 프로덕션용 환경 변수 파일을 만듭니다:

```bash
cd /Users/yoodongseok/Desktop/woorifisafinal/backend

# .env.production 파일 생성 (vi 또는 텍스트 에디터 사용)
nano .env.production
```

**`.env.production` 파일 내용:**

```bash
# 데이터베이스 설정 (RDS)
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your-database-password
DB_NAME=woorizip

# JWT 설정
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256

# Host
BACKEND_URI=0.0.0.0

# CORS 설정 (Frontend 도메인 허용)
CORS_ORIGINS=https://woorizip.info,https://www.woorizip.info,http://localhost:5173
```

> **⚠️ 중요:** 실제 값으로 변경하세요!
> - `DB_HOST`: RDS 엔드포인트
> - `DB_PASSWORD`: 실제 DB 비밀번호
> - `JWT_SECRET_KEY`: 강력한 랜덤 문자열

---

## 🔨 Step 2: Dockerfile 확인

이미 있는 Dockerfile을 확인합니다:

```dockerfile
# 1️⃣ 베이스 이미지
FROM python:3.11-slim AS base

WORKDIR /app

# 2️⃣ 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 3️⃣ uv 설치 및 의존성 설치
RUN pip install --upgrade pip && pip install uv \
    && uv pip install --system .

# 4️⃣ 애플리케이션 코드 복사
COPY . .

# 5️⃣ FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

✅ **이미 완벽합니다!**

---

## 📝 Step 3: .dockerignore 확인

`.dockerignore` 파일도 이미 있습니다:

```
.git
.venv
__pycache__
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
pytest_cache
tests
```

✅ **완벽합니다!**

---

## 🐳 Step 4: Docker 이미지 빌드

### 4-1. Docker Hub 사용자명 설정

```bash
export DOCKER_USERNAME=dongseok0610
```

### 4-2. 이미지 빌드 (Linux/AMD64용)

```bash
cd /Users/yoodongseok/Desktop/woorifisafinal/backend

# Multi-platform 빌드 및 푸시
docker buildx build \
  --platform linux/amd64 \
  -t ${DOCKER_USERNAME}/woorifisa-backend:latest \
  --push \
  .
```

**또는 버전 태그와 함께:**

```bash
docker buildx build \
  --platform linux/amd64 \
  -t ${DOCKER_USERNAME}/woorifisa-backend:latest \
  -t ${DOCKER_USERNAME}/woorifisa-backend:v1.0.0 \
  --push \
  .
```

---

## ☁️ Step 5: Docker Hub 확인

```bash
# Docker Hub 로그인 (필요시)
docker login

# 이미지 푸시 확인
# https://hub.docker.com/r/dongseok0610/woorifisa-backend
```

---

## 🖥️ Step 6: EC2 Backend 인스턴스 배포

### 6-1. Backend EC2 인스턴스 접속

**Bastion을 통한 SSH 접속:**

```bash
# Backend는 Private Subnet에 있으므로 Bastion 경유 필수
ssh -i "your-key.pem" -J ubuntu@[Bastion Public IP] ubuntu@10.0.2.10

# 또는 SSH config 설정했다면
ssh backend
```

### 6-2. Docker 설치 (처음 한 번만)

```bash
# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 로그아웃 후 재접속
exit
ssh -i "your-key.pem" -J ubuntu@[Bastion IP] ubuntu@10.0.2.10
```

### 6-3. 환경 변수 파일 생성

Backend EC2에서 `.env` 파일을 생성해야 합니다:

```bash
# Backend EC2에서 실행
mkdir -p ~/backend
cd ~/backend

# .env 파일 생성
nano .env
```

**`.env` 파일 내용 (로컬의 .env.production과 동일):**

```bash
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your-database-password
DB_NAME=woorizip

JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256

BACKEND_URI=0.0.0.0

CORS_ORIGINS=https://woorizip.info,https://www.woorizip.info,http://localhost:5173
```

저장: `Ctrl + X` → `Y` → `Enter`

### 6-4. Docker 이미지 Pull

```bash
# 최신 이미지 다운로드
docker pull dongseok0610/woorifisa-backend:latest

# 다운로드 확인
docker images | grep backend
```

### 6-5. 컨테이너 실행

```bash
# 기존 컨테이너 중지 및 삭제 (있는 경우)
docker stop woorifisa-backend 2>/dev/null || true
docker rm woorifisa-backend 2>/dev/null || true

# 새 컨테이너 실행
docker run -d \
  --name woorifisa-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file ~/backend/.env \
  dongseok0610/woorifisa-backend:latest

# 실행 확인
docker ps

# 로그 확인
docker logs --tail 50 woorifisa-backend

# 실시간 로그
docker logs -f woorifisa-backend
```

---

## ✅ Step 7: 배포 확인

### 7-1. 컨테이너 상태 확인

```bash
# 실행 중인지 확인
docker ps

# 예상 출력:
# CONTAINER ID   IMAGE                                   STATUS        PORTS
# abc123...      dongseok0610/woorifisa-backend:latest   Up 1 minute   0.0.0.0:8000->8000/tcp
```

### 7-2. Health Check

```bash
# Backend 인스턴스 내부에서
curl http://localhost:8000/docs

# 또는 간단한 엔드포인트
curl http://localhost:8000/
```

### 7-3. Frontend에서 접근 테스트

```bash
# Frontend 인스턴스에서 (또는 로컬에서)
curl http://10.0.2.10:8000/docs
```

### 7-4. 브라우저에서 확인

Frontend 웹사이트에서:
- 로그인 시도
- API 호출 확인
- 브라우저 Console (F12)에서 에러 없는지 확인

---

## 🔧 Step 8: Security Group 설정

Backend EC2 Security Group에서:

**Inbound Rules:**
```
Type        Protocol    Port    Source              Description
Custom TCP  TCP         8000    [Frontend SG ID]    From Frontend
Custom TCP  TCP         8000    [ALB SG ID]         From ALB (사용시)
SSH         TCP         22      [Bastion SG ID]     From Bastion
```

**Outbound Rules:**
```
All traffic → 0.0.0.0/0 (RDS, 외부 API 호출 가능)
```

---

## 🔄 Step 9: 업데이트 (코드 수정 후 재배포)

### 9-1. 로컬에서 재빌드

```bash
cd /Users/yoodongseok/Desktop/woorifisafinal/backend
export DOCKER_USERNAME=dongseok0610

# 버전 업데이트
docker buildx build \
  --platform linux/amd64 \
  -t ${DOCKER_USERNAME}/woorifisa-backend:latest \
  -t ${DOCKER_USERNAME}/woorifisa-backend:v1.0.1 \
  --push \
  .
```

### 9-2. EC2에서 업데이트

```bash
# Backend EC2 접속
ssh -i "key.pem" -J ubuntu@[Bastion IP] ubuntu@10.0.2.10

# 최신 이미지 pull
docker pull dongseok0610/woorifisa-backend:latest

# 무중단 배포
docker stop woorifisa-backend
docker rm woorifisa-backend
docker run -d \
  --name woorifisa-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file ~/backend/.env \
  dongseok0610/woorifisa-backend:latest

# 확인
docker ps
docker logs -f woorifisa-backend
```

---

## 📊 Step 10: 모니터링

### 로그 확인

```bash
# 최근 100줄
docker logs --tail 100 woorifisa-backend

# 실시간
docker logs -f woorifisa-backend

# 특정 시간 이후
docker logs --since 10m woorifisa-backend
```

### 리소스 사용량

```bash
# CPU, 메모리
docker stats woorifisa-backend

# 디스크 사용량
docker system df
```

### 컨테이너 내부 접속 (디버깅)

```bash
# 컨테이너 내부 쉘 접속
docker exec -it woorifisa-backend /bin/bash

# Python 인터프리터
docker exec -it woorifisa-backend python

# 로그 파일 확인
docker exec woorifisa-backend ls -la /app
```

---

## 🎯 완전 요약: 한눈에 보기

### 로컬 (Mac)

```bash
cd /Users/yoodongseok/Desktop/woorifisafinal/backend
export DOCKER_USERNAME=dongseok0610

# 이미지 빌드 및 푸시
docker buildx build \
  --platform linux/amd64 \
  -t ${DOCKER_USERNAME}/woorifisa-backend:latest \
  --push \
  .
```

### EC2 Backend 인스턴스

```bash
# SSH 접속
ssh -i "key.pem" -J ubuntu@[Bastion IP] ubuntu@10.0.2.10

# .env 파일 생성 (처음 한 번만)
mkdir -p ~/backend
nano ~/backend/.env
# (환경 변수 입력 후 저장)

# 배포
docker pull dongseok0610/woorifisa-backend:latest
docker stop woorifisa-backend || true
docker rm woorifisa-backend || true
docker run -d \
  --name woorifisa-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file ~/backend/.env \
  dongseok0610/woorifisa-backend:latest

# 확인
docker ps
docker logs woorifisa-backend
curl http://localhost:8000/docs
```

---

## ⚠️ 주의사항

1. **환경 변수 보안**
   - `.env` 파일에 실제 비밀번호 저장
   - Git에 커밋하지 말 것
   - EC2에서만 관리

2. **데이터베이스 연결**
   - RDS Security Group에서 Backend IP 허용
   - DB_HOST는 RDS 엔드포인트 사용

3. **포트 충돌**
   - 8000번 포트가 이미 사용 중이면 다른 포트 사용
   - MCP/Dummy API와 포트 충돌 주의

4. **CORS 설정**
   - Frontend 도메인을 정확히 입력
   - `https://` 프로토콜 주의

---

## 🔍 문제 해결

### 컨테이너가 시작 안 됨

```bash
# 로그 확인
docker logs woorifisa-backend

# 일반적인 원인:
# - .env 파일 경로 오류
# - 환경 변수 오타
# - 포트 충돌
```

### DB 연결 안 됨

```bash
# RDS Security Group 확인
# Backend EC2의 Private IP가 허용되어 있는지

# 컨테이너 내부에서 테스트
docker exec -it woorifisa-backend python
>>> import pymysql
>>> conn = pymysql.connect(host='...', user='admin', password='...')
```

### CORS 에러

```bash
# .env 파일 확인
cat ~/backend/.env | grep CORS

# 컨테이너 재시작
docker restart woorifisa-backend
```

---

## ✅ 배포 완료 체크리스트

- [ ] `.env.production` 파일 생성 (로컬)
- [ ] Docker 이미지 빌드 완료
- [ ] Docker Hub 푸시 완료
- [ ] Backend EC2 접속 가능
- [ ] `.env` 파일 생성 (EC2)
- [ ] Docker 컨테이너 실행 완료
- [ ] `docker ps`에서 실행 확인
- [ ] 로그에 에러 없음
- [ ] Frontend에서 API 호출 성공
- [ ] CORS 에러 없음

---

**이제 시작하세요!** 🚀
