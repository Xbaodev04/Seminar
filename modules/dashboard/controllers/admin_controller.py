from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["admin dashboard"])

@router.get("/")
def get_dashboard():
    return {"message": "Admin dashboard data"}
