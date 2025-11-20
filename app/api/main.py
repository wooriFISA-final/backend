from fastapi import APIRouter

from app.api.routes import member_endpoint, login_endpoint, report_endpoint

api_router = APIRouter()
api_router.include_router(login_endpoint.router)
api_router.include_router(member_endpoint.router)
api_router.include_router(report_endpoint.router)