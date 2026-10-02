from sqlalchemy.orm import Session
from models.stallContent import StallContent
from models.stallContentTranslation import StallContentTranslation
from typing import Optional, List, Dict

class MobileService:
    def __init__(self, db: Session):
        self.db = db

    # Lấy nội dung bài thuyết minh (audio, text) của một địa điểm theo ngôn ngữ (fallback về 'vi' nếu không có)
    def get_content_with_fallback(self, stall_id: str, language: str) -> List[Dict]:
        # Đầu tiên, kiểm tra xem stall_content có tồn tại không
        stall_content = self.db.query(StallContent).filter(StallContent.stall_id == stall_id).first()
        if not stall_content:
            return []
            
        from models.stall import Stall
        from models.stallTranslation import StallTranslation
        
        # Lấy thông tin địa điểm để làm tiêu đề dự phòng
        stall = self.db.query(Stall).filter(Stall.id == stall_id).first()
        title = stall.name if stall else ""
        
        # Tìm bản dịch của địa điểm để lấy tiêu đề
        stall_trans = self.db.query(StallTranslation).filter(
            StallTranslation.stall_id == stall_id,
            StallTranslation.language_code == language
        ).first()
        
        if not stall_trans:
            stall_trans = self.db.query(StallTranslation).filter(
                StallTranslation.stall_id == stall_id,
                StallTranslation.language_code == "vi"
            ).first()
            
        if stall_trans and stall_trans.name:
            title = stall_trans.name

        # Tìm bản dịch theo ngôn ngữ được yêu cầu
        translation = self.db.query(StallContentTranslation).filter(
            StallContentTranslation.stall_content_id == stall_content.id,
            StallContentTranslation.language_code == language
        ).first()

        if not translation:
            # Cơ chế dự phòng: Thử ngôn ngữ mặc định 'vi'
            translation = self.db.query(StallContentTranslation).filter(
                StallContentTranslation.stall_content_id == stall_content.id,
                StallContentTranslation.language_code == "vi"
            ).first()

            # Nếu vẫn không tìm thấy, lấy bất kỳ bản dịch nào hiện có để có dữ liệu trả về
            if not translation:
                translation = self.db.query(StallContentTranslation).filter(
                    StallContentTranslation.stall_content_id == stall_content.id
                ).first()

        # Xây dựng cấu trúc dữ liệu trả về
        response = {
            "id": stall_content.id,
            "stall_id": stall_id,
            "language_code": translation.language_code if translation else "vi",
            "title": title,
            "text_content": translation.tts_script if (translation and translation.tts_script) else stall_content.tts_script,
            "audio_url": translation.audio_url if translation else None,
            "duration": translation.audio_duration if translation else 0,
            "order": 1
        }
        
        return [response]
  
    # Lấy danh sách các ngôn ngữ khả dụng cho bài thuyết minh của một địa điểm cụ thể.
    def get_available_languages(self, stall_id: str) -> List[Dict]:
      
        stall_content = self.db.query(StallContent).filter(StallContent.stall_id == stall_id).first()
        if not stall_content:
            return []

        translations = self.db.query(StallContentTranslation.language_code).filter(
            StallContentTranslation.stall_content_id == stall_content.id
        ).all()

        return [{"language_code": t.language_code} for t in translations]
    
    # Lưu lại lịch sử nghe audio của người dùng 
    def save_listening_history(self, history_data: dict, user_id: Optional[str] = None) -> dict:
        from models.listeningHistory import ListeningHistory
        import time

        new_history = ListeningHistory(
            stall_id=history_data.get("stall_id"),
            stall_content_id=history_data.get("stall_content_id"),
            listened_at=history_data.get("listened_at", int(time.time())),
            listen_duration=history_data.get("listen_duration", 0),
            user_id=user_id,
            created_at=int(time.time()),
            updated_at=int(time.time())
        )
        self.db.add(new_history)
        self.db.commit()
        self.db.refresh(new_history)
        
        return {
            "id": new_history.id,
            "stall_id": new_history.stall_id,
            "stall_content_id": new_history.stall_content_id,
            "listened_at": new_history.listened_at,
            "listen_duration": new_history.listen_duration
        }
