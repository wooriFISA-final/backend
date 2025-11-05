from fastapi import FastAPI
from app.api.main import api_router
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
BACKEND_URI = os.getenv("BACKEND_URI")

app = FastAPI(
    title="backend server",
    description="API",
    version="1.0.0"
)

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:5173"] 처럼 프론트 주소
    allow_credentials=True,
    allow_methods=["*"],  # ✅ OPTIONS 포함 모든 메서드 허용
    allow_headers=["*"],
)