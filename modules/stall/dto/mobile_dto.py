from pydantic import BaseModel
from typing import Optional, List

class StallResponse(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    radius: int
    cover_image: Optional[str]
    category: Optional[str]
    price_range: Optional[str]
    opening_hours: Optional[str]
    close_hours: Optional[str]
    contact_phone: Optional[str]
    website: Optional[str]
    average_rating: float
    total_reviews: int
    distance: Optional[float] = None  # Returned when location is provided

    class Config:
        from_attributes = True

class StallListResponse(BaseModel):
    items: List[StallResponse]
    total: int
