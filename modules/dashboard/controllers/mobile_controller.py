from fastapi import APIRouter

router = APIRouter(prefix="/home", tags=["mobile home"])

@router.get("/")
def get_home():
    return {"message": "Mobile home feed data"}
