from fastapi import APIRouter
from api.v1.admin import router as admin_router
from api.v1.owner import router as owner_router
from api.v1.mobile import router as mobile_router

api_router = APIRouter()

api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(owner_router, prefix="/owner", tags=["owner"])
api_router.include_router(mobile_router, prefix="/mobile", tags=["mobile"])

