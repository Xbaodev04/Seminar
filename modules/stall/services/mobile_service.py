from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from models.stall import Stall
from models.stallTranslation import StallTranslation
from typing import Optional, Tuple, List
import math

class MobileService:
    def __init__(self, db: Session):
        self.db = db
    # Định dạng dữ liệu địa điểm
    def _format_stall(self, stall: Stall, trans: Optional[StallTranslation], lat: float = None, lng: float = None) -> dict:
        data = {
            "id": stall.id,
            "name": trans.name if trans and trans.name else stall.name,
            "latitude": stall.latitude,
            "longitude": stall.longitude,
            "radius": stall.radius,
            "cover_image": stall.cover_image,
            "category": trans.category if trans and trans.category else stall.category,
            "price_range": stall.price_range,
            "opening_hours": stall.opening_hours,
            "close_hours": stall.close_hours,
            "contact_phone": stall.contact_phone,
            "website": stall.website,
            "average_rating": float(stall.average_rating) if stall.average_rating else 0.0,
            "total_reviews": stall.total_reviews,
        }
        if lat is not None and lng is not None:
            data["distance"] = self._calculate_distance(lat, lng, stall.latitude, stall.longitude)
        return data
    # Lấy danh sách địa điểm theo keyword, tọa độ, giới hạn và offset
    def get_stalls(self, keyword: Optional[str] = None, lat: Optional[float] = None, lng: Optional[float] = None, limit: int = 20, offset: int = 0, language: str = "vi") -> Tuple[List[dict], int]:
        query = self.db.query(Stall, StallTranslation).outerjoin(
            StallTranslation, (Stall.id == StallTranslation.stall_id) & (StallTranslation.language_code == language)
        )

        if keyword:
            kw = f"%{keyword.lower()}%"
            query = query.filter(or_(func.lower(StallTranslation.name).like(kw), func.lower(Stall.name).like(kw)))
        # Khoảng cách giữa tọa độ của bạn và địa điểm
        dist_expr = None
        if lat is not None and lng is not None:
            dist_expr = 6371 * func.acos(func.cos(func.radians(lat)) * func.cos(func.radians(Stall.latitude)) * func.cos(func.radians(Stall.longitude) - func.radians(lng)) + func.sin(func.radians(lat)) * func.sin(func.radians(Stall.latitude)))
        # Đếm tổng số địa điểm
        total = query.count()
        # Sắp xếp theo khoảng cách hoặc theo ngày tạo
        query = query.order_by(dist_expr.asc()) if dist_expr is not None else query.order_by(Stall.created_at.desc())
        # Trả về danh sách địa điểm theo giới hạn và offset
        return [self._format_stall(s, t, lat, lng) for s, t in query.offset(offset).limit(limit).all()], total

    # Lấy thông tin địa điểm theo id
    def get_stall_by_id(self, stall_id: str, language: str = "vi") -> Optional[dict]:
        result = self.db.query(Stall, StallTranslation).outerjoin(
            StallTranslation, (Stall.id == StallTranslation.stall_id) & (StallTranslation.language_code == language)
        ).filter(Stall.id == stall_id).first()
        
        return self._format_stall(result[0], result[1]) if result else None

    # Tính khoảng cách giữa hai tọa độ
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Bán kính Trái Đất theo km
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dLon / 2) * math.sin(dLon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
