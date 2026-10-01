# Seminar API - Base Project 🚀

Dự án này được khởi tạo dựa trên kiến trúc của `ans_api-main`, kết nối tới database `seminar_db`.

## ⚙️ Cấu trúc thư mục

- `api/`: Chứa các endpoint router theo từng role.
  - `admin/`: API dành cho admin (Quản trị viên)
  - `owner/`: API dành cho owner (Chủ gian hàng/khách sạn...)
  - `mobile/`: API dành cho mobile app (Customer/Khách hàng)
- `core/`: Chứa file cấu hình config, database connection, security.
- `models/`: Chứa các SQLAlchemy models map với các bảng trong cơ sở dữ liệu.
- `utils/`: Chứa các hàm tiện ích dùng chung.
- `.env`: File cấu hình môi trường.
- `main.py`: File entrypoint chính của FastAPI.
- `alembic/`: Thư mục quản lý phiên bản database migrations.

## 🛠 Hướng dẫn chạy local

1. Đảm bảo bạn đã có MySQL và tạo database `seminar_db`:
```sql
CREATE DATABASE seminar_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Cài đặt môi trường ảo (virtualenv):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

4. Cập nhật cấu hình trong `.env` cho đúng với local của bạn:
```ini
DATABASE_URL=mysql+pymysql://root:password@localhost/seminar_db
```

5. Khởi tạo Database schema bằng Alembic (Tạo các bảng từ thư mục `models`):
```bash
alembic revision --autogenerate -m "Init seminar_db"
alembic upgrade head
```

6. Chạy server phát triển:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API Docs: `http://localhost:8000/docs`
- Các endpoint đã được khai báo với 3 prefix:
  - `/api/v1/admin`
  - `/api/v1/owner`
  - `/api/v1/mobile`

## 💡 Ghi chú
Các models được kế thừa và copy từ `ans_api-main` để giữ nguyên các bảng tương tự. Bạn có thể xóa/chỉnh sửa các model không cần thiết trong thư mục `models/` cho phù hợp với dự án `seminar_db`.
