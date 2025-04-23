# Employee Management System

## Giới thiệu
Ứng dụng quản lý nhân viên sử dụng SQLAlchemy ORM với PostgreSQL, FastAPI và Native SQL.

## Tính năng
- 🏢 Quản lý phòng ban
- 👥 Quản lý nhân viên
- 🔍 Tìm kiếm nhân viên
- 📊 Thống kê theo phòng ban
- 🌐 REST API
- 📝 Native SQL Queries

## Cấu trúc Project
```
ORM_python/
├── main.py          # CLI commands và ORM models
├── api.py           # FastAPI server
├── SQL.py           # Native SQL queries
├── .env            # Environment variables
└── README.md       # Documentation
```

## Mô hình dữ liệu
### Department
- id: Integer (Primary Key)
- name: String
- created_at: DateTime
- updated_at: DateTime

### Employee
- id: Integer (Primary Key)
- first_name: String
- last_name: String
- email: String (Unique)
- department_id: Integer (Foreign Key)
- hire_date: DateTime
- created_at: DateTime
- updated_at: DateTime

## Hướng dẫn cài đặt
1. Clone repository
2. Tạo virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Tạo file .env:
```
DATABASE_URL=postgresql://username:password@localhost:5432/orm_example
```

5. Khởi tạo database:
```bash
python main.py init-db
```

## Sử dụng CLI Commands
1. Tạo dữ liệu mẫu:
```bash
python main.py generate-sample-data --num-departments 20 --num-employees 1000
```

2. Liệt kê phòng ban:
```bash
python main.py list-departments
```

3. Liệt kê nhân viên:
```bash
python main.py list-employees
```

## Sử dụng Native SQL (SQL.py)
1. Thống kê theo phòng ban:
```python
from SQL import get_department_stats
get_department_stats()
```

2. Tìm kiếm nhân viên:
```python
from SQL import search_employees
search_employees("john")  # Tìm nhân viên có tên John
```

3. Xem danh sách nhân viên theo phòng ban:
```python
from SQL import get_employee_list
get_employee_list("Engineering", 10)  # 10 nhân viên mới nhất của phòng Engineering
```

4. Thêm nhân viên mới:
```python
from SQL import add_employee
add_employee("John", "Doe", "john.doe@company.com", "Engineering")
```

## Sử dụng REST API (api.py)
1. Khởi động server:
```bash
cd Day2/ORM_python
python api.py
```

2. API Endpoints:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Departments API
```bash
# Lấy danh sách phòng ban
curl -X GET http://localhost:8000/api/departments

# Tạo phòng ban mới
curl -X POST http://localhost:8000/api/departments \
  -H "Content-Type: application/json" \
  -d '{"name": "Engineering"}'

# Cập nhật phòng ban
curl -X PUT http://localhost:8000/api/departments/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Software Engineering"}'

# Xóa phòng ban
curl -X DELETE http://localhost:8000/api/departments/1
```

### Employees API
```bash
# Lấy danh sách nhân viên
curl -X GET http://localhost:8000/api/employees

# Lấy danh sách nhân viên theo phòng ban
curl -X GET "http://localhost:8000/api/employees?department=Engineering"

# Tạo nhân viên mới
curl -X POST http://localhost:8000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@company.com",
    "department_id": 1
  }'

# Cập nhật thông tin nhân viên
curl -X PUT http://localhost:8000/api/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@company.com",
    "department_id": 2
  }'

# Xóa nhân viên
curl -X DELETE http://localhost:8000/api/employees/1
```

### Các API Khác
```bash
# Tạo dữ liệu mẫu
curl -X POST http://localhost:8000/api/generate-sample-data \
  -H "Content-Type: application/json" \
  -d '{"num_departments": 5, "num_employees": 20}'

# Thống kê
curl -X GET http://localhost:8000/api/stats
```

## So sánh với Prisma
1. **Schema Definition**: SQLAlchemy sử dụng Python classes, Prisma sử dụng schema file
2. **Type Safety**: Prisma có type safety tốt hơn với TypeScript
3. **Query Builder**: SQLAlchemy linh hoạt hơn với raw SQL
4. **Migration**: Prisma có công cụ migration tốt hơn

## Đóng góp
1. Fork repository
2. Tạo branch mới
3. Commit changes
4. Tạo Pull Request

## Giấy phép
MIT License 