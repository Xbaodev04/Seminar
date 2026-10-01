from fastapi import APIRouter
from modules.dashboard.controllers.admin_controller import router as dashboard_router

router = APIRouter()
router.include_router(dashboard_router)
