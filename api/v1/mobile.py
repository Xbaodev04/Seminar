from fastapi import APIRouter
from modules.auth.controllers.mobile_controller import router as auth_router
from modules.dashboard.controllers.mobile_controller import router as home_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(home_router)
