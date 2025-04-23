# API Examples với cURL

## Departments API

### 1. Lấy danh sách phòng ban
```bash
curl -X GET http://localhost:8000/api/departments
```

### 2. Lấy thông tin một phòng ban
```bash
curl -X GET http://localhost:8000/api/departments/1
```

### 3. Tạo phòng ban mới
```bash
curl -X POST http://localhost:8000/api/departments \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering"
  }'
```

### 4. Cập nhật phòng ban
```bash
curl -X PUT http://localhost:8000/api/departments/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Software Engineering"
  }'
```

### 5. Xóa phòng ban
```bash
curl -X DELETE http://localhost:8000/api/departments/1
```

## Employees API

### 1. Lấy danh sách nhân viên
```bash
curl -X GET http://localhost:8000/api/employees
```

### 2. Lấy danh sách nhân viên theo phòng ban
```bash
curl -X GET http://localhost:8000/api/employees?department=Engineering
```

### 3. Lấy thông tin một nhân viên
```bash
curl -X GET http://localhost:8000/api/employees/1
```

### 4. Tạo nhân viên mới
```bash
curl -X POST http://localhost:8000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "department_id": 1
  }'
```

### 5. Cập nhật thông tin nhân viên
```bash
curl -X PUT http://localhost:8000/api/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "department_id": 2
  }'
```

### 6. Xóa nhân viên
```bash
curl -X DELETE http://localhost:8000/api/employees/1
```

## Các API Khác

### 1. Tạo dữ liệu mẫu
```bash
curl -X POST http://localhost:8000/api/generate-sample-data \
  -H "Content-Type: application/json" \
  -d '{
    "num_departments": 5,
    "num_employees": 20
  }'
```

### 2. Thống kê
```bash
curl -X GET http://localhost:8000/api/stats
```

## Response Examples

### Department Response
```json
{
  "id": 1,
  "name": "Engineering",
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z",
  "employee_count": 5
}
```

### Employee Response
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "department": {
    "id": 1,
    "name": "Engineering"
  },
  "hire_date": "2024-03-15T10:30:00Z",
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z"
}
```

### Stats Response
```json
{
  "total_departments": 5,
  "total_employees": 20,
  "departments": [
    {
      "name": "Engineering",
      "employee_count": 8
    },
    {
      "name": "Marketing",
      "employee_count": 5
    }
  ]
}
```

## Error Response
```json
{
  "error": "Not Found",
  "message": "Department with ID 1 not found",
  "status_code": 404
}
``` 