from pydantic import BaseModel
from typing import Optional, List

class StallContentResponse(BaseModel):
    id: str
    stall_id: str
    language_code: str
    audio_url: Optional[str]
    audio_duration: Optional[int]
    audio_file_size: Optional[int]
    tts_script: Optional[str]
    is_fallback: bool

    class Config:
        from_attributes = True
        
class AvailableLanguageResponse(BaseModel):
    language_code: str
    
class AvailableLanguagesResponse(BaseModel):
    languages: List[AvailableLanguageResponse]

class ListeningHistoryCreate(BaseModel):
    stall_id: str
    stall_content_id: str
    listened_at: int
    listen_duration: int

