from fastapi import FastAPI
from app.api.main import api_router
from dotenv import load_dotenv
import os

load_dotenv()
BACKEND_URI = os.getenv("BACKEND_URI")

app = FastAPI(
    title="backend server",
    description="API",
    version="1.0.0"
)

app.include_router(api_router)