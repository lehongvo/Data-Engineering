# BigQuery Partitioning Exercise

## Mục đích

Project này giúp bạn thực hành các kỹ thuật quản lý và tối ưu truy vấn dữ liệu lớn với BigQuery Partitioning & Clustering. Bạn sẽ:
- Tạo các bảng partitioned với nhiều kiểu khác nhau
- Sinh dữ liệu mẫu tự động
- Phân tích metadata partition và so sánh hiệu năng truy vấn
- Thực hành truy vấn tối ưu với partition filter

## Yêu cầu
- Python 3.7+
- Google Cloud SDK đã cài đặt và cấu hình (`gcloud auth login`)
- Quyền truy cập BigQuery

## Hướng dẫn sử dụng

### 1. Clone repository và cài đặt
```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Chạy script tự động
```bash
chmod +x run.sh
./run.sh
```
Script sẽ:
- Tạo môi trường ảo Python
- Cài các package cần thiết (`google-cloud-bigquery`, `pandas`, `matplotlib`, `faker`, `db-dtypes`)
- Tạo dataset và các bảng partitioned mẫu
- Sinh và insert 200 record random cho mỗi bảng
- Phân tích metadata partition, so sánh hiệu năng truy vấn
- Sinh các biểu đồ vào thư mục `data/`

### 3. Các file chính
- `run.sh`: Script tự động setup và chạy toàn bộ bài tập
- `create_partitioned_table.py`: Tạo bảng partitioned và sinh dữ liệu mẫu
- `partition_metadata.py`: Phân tích metadata partition, so sánh hiệu năng truy vấn
- `sample_queries.sql`: Một số truy vấn mẫu tối ưu với partition filter
- `data/`: Chứa các file ảnh biểu đồ kết quả

### 4. Lưu ý
- Đảm bảo đã cấu hình đúng Google Cloud project (`gcloud config set project <YOUR_PROJECT_ID>`)
- Nếu muốn làm lại từ đầu, xóa các bảng/dataset trên BigQuery và chạy lại script
- Có thể chỉnh sửa schema, số lượng record, hoặc truy vấn mẫu theo ý bạn

### 5. Tham khảo
- [BigQuery Partitioned Tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
- [BigQuery Clustering](https://cloud.google.com/bigquery/docs/clustered-tables)

---

Nếu gặp lỗi hoặc cần hỗ trợ, hãy tạo issue hoặc liên hệ tác giả!