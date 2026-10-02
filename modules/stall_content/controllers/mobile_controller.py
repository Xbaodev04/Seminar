from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from common.dto.response import success_response
from modules.stall_content.services.mobile_service import MobileService
from modules.stall_content.dto.mobile_dto import StallContentResponse, AvailableLanguagesResponse, ListeningHistoryCreate
from utils.security import jwt, SECRET_KEY, ALGORITHM
from models.user import User

router = APIRouter(prefix="/stalls/{stall_id}/content", tags=["Stall Content Mobile"])

@router.get("", response_model=None)
def get_stall_content(
    stall_id: str,
    # Lấy nội dung bài thuyết minh (audio, text) của một địa điểm theo ngôn ngữ (fallback về 'vi' nếu không có)
    accept_language: str = Header("vi"),
    db: Session = Depends(get_db)
):
    locale = accept_language.split(",")[0].split("-")[0] if accept_language else "vi"
    
    service = MobileService(db)
    content = service.get_content_with_fallback(stall_id, language=locale)
    
    if content is None:
        raise HTTPException(status_code=404, detail="Stall content not found")
        
    return success_response(
        message="Success",
        data=content
    )

@router.get("/available-languages", response_model=None)
def get_available_languages(
    stall_id: str,
    # Lấy danh sách các ngôn ngữ (vi, en, ...) hiện có bản dịch cho bài thuyết minh của địa điểm này
    db: Session = Depends(get_db)
):
    service = MobileService(db)
    languages = service.get_available_languages(stall_id)
    
    return success_response(
        message="Get available languages success",
        data={"languages": languages}
    )

history_router = APIRouter(prefix="/listening-history", tags=["Listening History Mobile"])
security = HTTPBearer(auto_error=False)

def get_current_user_optional(
    # Dependency để lấy thông tin user hiện tại nếu có truyền token (không bắt buộc đăng nhập)
    credentials: HTTPAuthorizationCredentials | None = Depends(security), 
    db: Session = Depends(get_db)
):
    if not credentials:
        return None
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id:
            return db.query(User).filter(User.id == user_id).first()
    except Exception:
        pass
    return None

@history_router.post("", response_model=None)
def save_listening_history(
    payload: ListeningHistoryCreate,
    # Lưu lại lịch sử/thời lượng nghe audio của người dùng 
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    service = MobileService(db)
    user_id = current_user.id if current_user else None
    
    try:
        data = service.save_listening_history(payload.dict(), user_id=user_id)
        return success_response(
            message="Success",
            data=data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
