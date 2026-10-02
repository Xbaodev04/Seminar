from fastapi import APIRouter
from modules.auth.controllers.mobile_controller import router as auth_router
from modules.dashboard.controllers.mobile_controller import router as home_router
from modules.stall.controllers.mobile_controller import router as stall_router
from modules.stall_content.controllers.mobile_controller import router as stall_content_router

from modules.stall_content.controllers.mobile_controller import router as stall_content_router, history_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(home_router)
router.include_router(stall_router)
router.include_router(stall_content_router)
router.include_router(history_router)
