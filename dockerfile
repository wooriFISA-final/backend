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
