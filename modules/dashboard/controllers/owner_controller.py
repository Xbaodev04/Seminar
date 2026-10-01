from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["owner dashboard"])

@router.get("/")
def get_dashboard():
    return {"message": "Owner dashboard data"}
