from fastapi import APIRouter, Depends, Query, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from core.database import get_db
from common.dto.response import success_response
from modules.stall.services.mobile_service import MobileService
from modules.stall.dto.mobile_dto import StallListResponse, StallResponse

router = APIRouter(prefix="/stalls", tags=["Stalls Mobile"])

@router.get("", response_model=None)
def get_stalls(
    # Lấy danh sách các địa điểm (có hỗ trợ tìm kiếm, phân trang và sắp xếp theo khoảng cách nếu có toạ độ)
    keyword: Optional[str] = Query(None, description="Search keyword for stall name or category"),
    lat: Optional[float] = Query(None, description="User's latitude"),
    lng: Optional[float] = Query(None, description="User's longitude"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    accept_language: str = Header("vi"),
    db: Session = Depends(get_db)
):
    locale = accept_language.split(",")[0].split("-")[0] if accept_language else "vi"
    
    service = MobileService(db)
    items, total = service.get_stalls(
        keyword=keyword,
        lat=lat,
        lng=lng,
        limit=limit,
        offset=offset,
        language=locale
    )
    
    return success_response(
        message="Get stalls success",
        data={
            "items": items,
            "total": total
        }
    )

@router.get("/{stall_id}", response_model=None)
def get_stall_detail(
    stall_id: str,
    # Lấy thông tin chi tiết của một địa điểm (id, tên, toạ độ, hình ảnh, giờ mở cửa...) theo ngôn ngữ
    accept_language: str = Header("vi"),
    db: Session = Depends(get_db)
):
    locale = accept_language.split(",")[0].split("-")[0] if accept_language else "vi"
    
    service = MobileService(db)
    stall = service.get_stall_by_id(stall_id, language=locale)
    
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")
        
    return success_response(
        message="Get stall detail success",
        data=stall
    )
