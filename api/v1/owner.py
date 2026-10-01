from fastapi import APIRouter
from modules.auth.controllers.owner_controller import router as auth_router
from modules.dashboard.controllers.owner_controller import router as dashboard_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(dashboard_router)
