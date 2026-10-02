import os
import uuid
from datetime import datetime
import importlib
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Tạo thư mục chứa file audio
AUDIOS_DIR = Path(__file__).parent.parent / "audios"
AUDIOS_DIR.mkdir(exist_ok=True)

def generate_audio_from_text(text: str, language_code: str = "vi", return_bytes: bool = False) -> dict:
    """
    Tạo file audio từ văn bản bằng Google Text-to-Speech và upload lên Cloudinary.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    try:
        # Tạo tên file duy nhất
        audio_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.mp3"
        audio_path = AUDIOS_DIR / audio_filename
        
        # Tạo audio bằng gTTS
        tts = gTTS(text=text, lang=language_code, slow=False)
        tts.save(str(audio_path))
        
        # Lấy kích thước file
        file_size = audio_path.stat().st_size
        
        # Lấy thời lượng bằng pydub
        duration_seconds = None
        try:
            audio = AudioSegment.from_mp3(str(audio_path))
            duration_seconds = len(audio) // 1000
        except Exception as e:
            print(f"Lỗi khi lấy thời lượng audio: {str(e)}. Thời lượng sẽ được đặt thành None.")
        
        if return_bytes:
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            audio_path.unlink()
            return {
                "audio_bytes": audio_bytes,
                "audio_duration": duration_seconds,
                "audio_file_size": file_size,
            }
        else:
            # Upload lên Cloudinary
            upload_result = cloudinary.uploader.upload(
                str(audio_path),
                resource_type="video",
                folder="seminar_audios",
                public_id=audio_filename.split(".")[0]
            )
            # Xóa file tạm
            audio_path.unlink()
            
            return {
                "audio_url": upload_result.get("secure_url"),
                "audio_duration": duration_seconds,
                "audio_file_size": file_size,
            }
    except Exception as e:
        raise RuntimeError(f"Failed to generate audio: {str(e)}")


def delete_audio_file(audio_url: str) -> bool:
    # Xóa file audio
    if not audio_url or not audio_url.startswith("/audios/"):
        return False
    # Lấy tên file
    try:
        filename = audio_url.split("/")[-1]
        audio_path = AUDIOS_DIR / filename
        # Kiểm tra file có tồn tại không
        if audio_path.exists():
            audio_path.unlink()
            return True
        # Trả về False nếu file không tồn tại
        return False
    except Exception as e:
        print(f"Lỗi xóa file audio: {e}")
        return False
