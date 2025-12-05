from fastapi import FastAPI
from app.api.main import api_router
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import List

load_dotenv()
BACKEND_URI = os.getenv("BACKEND_URI")

# CORS 설정: 환경 변수에서 허용할 origins 가져오기
cors_origins_str = os.getenv(
    "CORS_ORIGINS",
    "http://woorizip.info,https://woorizip.info,https://www.woorizip.info,http://localhost:3000,http://localhost:5173"
)
allowed_origins: List[str] = [origin.strip() for origin in cors_origins_str.split(",")]

app = FastAPI(
    title="backend server",
    description="API",
    version="1.0.0"
)

app.include_router(api_router)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # 환경 변수로 관리되는 origins
    allow_credentials=True,
    allow_methods=["*"],  # OPTIONS 포함 모든 메서드 허용
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Preflight 요청 캐시 시간
)