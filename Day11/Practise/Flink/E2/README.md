# Bài tập 2: Phân tích dữ liệu truy cập web với Apache Flink

## Mục tiêu
Bài tập này nhằm thực hành các kỹ thuật:
- Windowing (cửa sổ thời gian)
- Filtering (lọc dữ liệu)
- Aggregations (tổng hợp dữ liệu)

## Mô tả
Ứng dụng này phân tích dữ liệu log truy cập web theo thời gian thực với các yêu cầu sau:
1. Lọc các requests lỗi (status code >= 400)
2. Tính số lượng truy cập theo URL trong cửa sổ thời gian 10 phút
3. Phát hiện các địa chỉ IP có số lượng requests lỗi bất thường

## Cấu trúc thư mục
- **code/**
  - `generate_logs.py`: Script tạo dữ liệu giả lập log truy cập web
  - `web_log_analysis.py`: Ứng dụng Flink phân tích dữ liệu
  - `requirements.txt`: Các thư viện Python cần thiết
- **data/**: Thư mục chứa dữ liệu đầu vào và kết quả
- `docker-compose.yml`: Cấu hình Docker cho môi trường Flink
- `run.sh`: Script thực thi ứng dụng

## Các bước thực hiện

### 1. Thiết lập môi trường
```bash
chmod +x run.sh
./run.sh
```
Chọn tùy chọn 3 để thiết lập môi trường Flink.

### 2. Tạo dữ liệu giả lập
Từ menu, chọn tùy chọn 1 để tạo dữ liệu giả lập. Script sẽ tạo ra 5000 bản ghi log truy cập web với các trường:
- IP address
- URL
- Timestamp
- Status code

### 3. Chạy ứng dụng phân tích
Từ menu, chọn tùy chọn 2 để chạy ứng dụng Flink phân tích dữ liệu.

### 4. Xem kết quả
Chọn tùy chọn 5 để xem kết quả phân tích, bao gồm:
- Danh sách các requests lỗi
- Số lượng truy cập theo URL trong cửa sổ 10 phút
- Các địa chỉ IP có hành vi bất thường (quá nhiều lỗi)

## Kiến thức Flink áp dụng

### 1. Event Time Processing
```python
event_time AS TO_TIMESTAMP(timestamp, 'yyyy-MM-dd HH:mm:ss'),
WATERMARK FOR event_time AS event_time - INTERVAL '5' SECONDS
```
Sử dụng timestamp từ dữ liệu log để xử lý theo thời gian thực sự của sự kiện, không phải thời gian nhận được.

### 2. Windowing với TUMBLE
```sql
FROM TABLE(
    TUMBLE(TABLE web_logs, DESCRIPTOR(event_time), INTERVAL '10' MINUTES))
```
Sử dụng cửa sổ thời gian cố định 10 phút để tính toán số lượng truy cập.

### 3. Filtering
```sql
WHERE status_code >= 400
```
Lọc các requests lỗi với status code từ 400 trở lên.

### 4. Aggregations
```sql
COUNT(*) AS access_count
```
Tính tổng số lượng truy cập theo URL và thời gian.

### 5. Phát hiện Anomaly (bất thường)
```sql
GROUP BY ip
HAVING COUNT(*) > 5
```
Tìm các địa chỉ IP có nhiều hơn 5 lần truy cập lỗi.

## Giao diện quản lý Flink
Bạn có thể truy cập dashboard Flink tại http://localhost:8082 để:
- Theo dõi trạng thái các jobs
- Xem chi tiết thực thi
- Theo dõi metrics và logs

## Mở rộng
Bạn có thể mở rộng bài tập này bằng cách:
1. Thêm nhiều loại phân tích khác nhau (ví dụ: phân tích user agent, quốc gia, ...)
2. Sử dụng cửa sổ trượt (sliding window) thay vì cửa sổ cố định
3. Tích hợp với Kafka để xử lý dữ liệu theo thời gian thực
4. Thêm trực quan hóa kết quả với Grafana hoặc các công cụ khác 