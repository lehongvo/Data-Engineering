# BigQuery API Project - Exercise 1

Project này xây dựng một RESTful API để tương tác với Google BigQuery, cho phép import dữ liệu, truy vấn và phân tích cơ hội bán hàng (sales opportunities).

## Cấu trúc Project

```
Exercise1/
├── api/                  # API package
│   ├── __init__.py       # Package initialization
│   ├── bigquery_service.py # BigQuery service class
│   └── fastapi_app.py    # FastAPI application
├── config/               # Configuration files
│   └── cgp-service-account-key.json  # Google Cloud service account key
├── data/                 # Sample data files
│   └── sales-data.csv    # Dữ liệu mẫu về cơ hội bán hàng
├── queries/              # SQL queries for analysis
│   └── analysis.sql      # Các truy vấn phân tích mẫu
├── main.py               # Main entry point
├── example_client.py     # Example client
├── requirements.txt      # Python dependencies
└── run.sh                # Script to run the application
```

## Kiến trúc

Project được tổ chức theo mô hình module tách biệt với cấu trúc như sau:

1. **main.py**: Entry point cho ứng dụng, xử lý tham số dòng lệnh và khởi động server
2. **api/bigquery_service.py**: Service layer cung cấp các phương thức tương tác với BigQuery
3. **api/fastapi_app.py**: API layer xử lý HTTP requests và responses
4. **queries/analysis.sql**: Các truy vấn SQL mẫu để phân tích dữ liệu cơ hội bán hàng
5. **example_client.py**: Client mẫu để tương tác với API

## Cài đặt và Chạy

### Yêu cầu

- Python 3.8+
- Google Cloud SDK
- Google Cloud account with BigQuery enabled
- Service account key với quyền BigQuery

### Cài đặt

1. Chuẩn bị service account key:
   - Tạo service account key từ Google Cloud Console
   - Lưu file key vào thư mục `config/cgp-service-account-key.json`

2. Chạy ứng dụng:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

3. Hoặc chạy trực tiếp:
   ```bash
   # Khởi động API
   python main.py --reload
   
   # Hoặc import dữ liệu mẫu và khởi động API
   python main.py --reload --import-data
   ```

4. Truy cập API documentation:
   ```
   http://localhost:8000/docs
   ```

## Sử dụng Client Example

Chúng tôi cung cấp một client mẫu để tương tác với API. Đây là cách sử dụng:

```bash
# Import CSV file vào BigQuery
python example_client.py import PATH_TO_CSV_FILE

# Lấy dữ liệu từ table (mặc định 10 rows)
python example_client.py data TABLE_ID

# Lấy dữ liệu với số rows cụ thể
python example_client.py data TABLE_ID 100

# Lấy schema của table
python example_client.py schema TABLE_ID

# Chạy truy vấn SQL
python example_client.py query "SELECT * FROM PROJECT_ID.exercise1.TABLE_ID LIMIT 10"

# Kiểm tra health của API
python example_client.py health
```

## API Endpoints

### 1. Import CSV vào BigQuery

```
POST /import-csv/
```

Upload file CSV để import vào BigQuery với schema tự động phát hiện.

### 2. Lấy dữ liệu từ table

```
GET /data/{table_id}?limit=10
```

Lấy dữ liệu từ table với giới hạn số rows tùy chọn.

### 3. Lấy schema của table

```
GET /schema/{table_id}
```

Lấy thông tin schema của table.

### 4. Chạy truy vấn SQL tùy chỉnh

```
POST /run-query/
```

Chạy truy vấn SQL tùy chỉnh và trả về kết quả.

### 5. Kiểm tra health

```
GET /health
```

Kiểm tra trạng thái API.

## Cấu trúc Dữ liệu Sales Opportunities

Dataset `sales-data_data` chứa thông tin về các cơ hội bán hàng với các trường sau:

- **Date**: Ngày tạo cơ hội
- **Salesperson**: Nhân viên bán hàng
- **Lead Name**: Tên khách hàng tiềm năng
- **Segment**: Phân khúc thị trường (SMB, Enterprise, Startup)
- **Region**: Khu vực địa lý
- **Target Close**: Ngày dự kiến đóng deal
- **Forecasted Monthly Revenue**: Doanh thu dự kiến hàng tháng
- **Opportunity Stage**: Giai đoạn của cơ hội (Closed Lost, Closed Won, etc.)
- **Weighted Revenue**: Doanh thu đã điều chỉnh theo xác suất
- **Closed Opportunity**: Cơ hội đã đóng hay chưa (true/false)
- **Active Opportunity**: Cơ hội còn đang hoạt động không (true/false)
- **Latest Status Entry**: Bản ghi có phải là cập nhật trạng thái mới nhất không (true/false)

## Ví dụ Truy vấn SQL

File `queries/analysis.sql` chứa các ví dụ truy vấn để phân tích dữ liệu cơ hội bán hàng:

1. **Tổng doanh thu theo phân khúc thị trường**: Phân tích tổng doanh thu và số lượng cơ hội theo từng phân khúc thị trường.

2. **Xu hướng doanh số theo ngày**: Theo dõi doanh thu và số lượng cơ hội theo thời gian.

3. **Top nhân viên bán hàng hiệu quả nhất**: Xác định những nhân viên bán hàng có thành tích tốt nhất dựa trên doanh thu.

4. **Phân tích theo giai đoạn cơ hội**: Đánh giá hiệu suất bán hàng theo các giai đoạn khác nhau của cơ hội.

5. **Hiệu suất theo khu vực**: So sánh hiệu suất bán hàng giữa các khu vực địa lý.

6. **Phân tích cơ hội đang hoạt động và đã đóng**: So sánh cơ hội đang hoạt động và đã đóng.

7. **Hiệu suất phân khúc theo khu vực**: Phân tích mối quan hệ giữa phân khúc thị trường và khu vực địa lý.

8. **Phân tích doanh thu dự kiến theo tháng**: Đánh giá xu hướng doanh thu dự kiến theo thời gian.

## Troubleshooting

Nếu gặp lỗi, hãy kiểm tra:
1. Service account key có đúng định dạng và quyền
2. BigQuery API đã được bật
3. Python version tương thích
4. Package db-dtypes đã được cài đặt (cần thiết cho xử lý kiểu dữ liệu của BigQuery)