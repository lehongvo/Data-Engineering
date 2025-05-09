# Apache Flink WordCount (E1)

Bài tập này triển khai một ứng dụng đơn giản đếm từ (WordCount) sử dụng Apache Flink. Ứng dụng đọc dữ liệu từ một file văn bản, đếm số lần xuất hiện của mỗi từ, và lưu kết quả vào file.

## Kiến trúc

Hệ thống bao gồm các thành phần:

- **JobManager**: Điều phối các tác vụ Flink, quản lý lỗi, theo dõi tiến trình
- **TaskManager**: Thực thi các tác vụ
- **Python API**: Sử dụng PyFlink để thực hiện xử lý dữ liệu

## Yêu cầu

- Docker & Docker Compose
- Python 3.7+
- pip3

## Cách chạy ứng dụng

Chúng tôi đã tạo một script để tiện cho việc thiết lập và chạy ứng dụng:

```bash
# Cấp quyền thực thi cho script
chmod +x run.sh

# Chạy script
./run.sh
```

Script sẽ hiển thị menu với các tùy chọn:

1. **Thiết lập môi trường**: Cài đặt các gói phụ thuộc, khởi động Flink
2. **Chạy WordCount**: Thực thi công việc đếm từ trên file đầu vào
3. **Mở Flink Dashboard**: Hướng dẫn truy cập giao diện web Flink để theo dõi
4. **Xem kết quả WordCount**: Hiển thị kết quả đếm từ

## Quy trình làm việc thông thường

1. Chọn tùy chọn 1 để thiết lập môi trường và khởi động Flink
2. Chọn tùy chọn 2 để chạy ứng dụng WordCount
3. Chọn tùy chọn 3 để mở Flink Dashboard và xem trạng thái
4. Chọn tùy chọn 4 để xem kết quả đếm từ chi tiết

## Cấu trúc thư mục

```
E1/
├── code/               # Thư mục chứa mã nguồn
│   └── word_count.py   # Chương trình WordCount
├── data/               # Thư mục dữ liệu
│   ├── input.txt       # File văn bản đầu vào
│   └── output/         # Thư mục chứa kết quả (được tạo sau khi chạy)
├── docker-compose.yml  # Cấu hình Docker Compose
├── requirements.txt    # Các gói Python cần thiết
├── run.sh              # Script để chạy ứng dụng
└── README.md           # File này
```

## Chi tiết triển khai

### 1. Đọc dữ liệu

Ứng dụng sử dụng Flink Table API để đọc dữ liệu từ file văn bản, xác định bảng với DDL:

```python
CREATE TABLE input_table (
    line STRING
) WITH (
    'connector' = 'filesystem',
    'path' = '/data/input.txt',
    'format' = 'text'
)
```

### 2. Xử lý dữ liệu

Chương trình thực hiện các bước:
- Sử dụng UDF (User-Defined Function) để tách dòng văn bản thành các từ
- Đếm số lần xuất hiện của mỗi từ
- Sử dụng SQL để thực hiện tính toán

```python
SELECT word, COUNT(*) as count
FROM (
    SELECT word
    FROM input_table,
    LATERAL TABLE(tokenize(line)) AS T(word)
    WHERE word <> ''
)
GROUP BY word
```

### 3. Ghi kết quả

Kết quả được lưu vào file CSV:

```python
CREATE TABLE output_table (
    word STRING,
    count BIGINT
) WITH (
    'connector' = 'filesystem',
    'path' = '/data/output',
    'format' = 'csv'
)
```

## Xử lý lỗi

Nếu bạn gặp vấn đề:

1. Kiểm tra log của container: `docker logs flink-jobmanager`
2. Đảm bảo cổng 8081 không bị sử dụng bởi ứng dụng khác
3. Kiểm tra quyền truy cập thư mục data và code
4. Hãy thử khởi động lại các container: `docker-compose down && docker-compose up -d` 