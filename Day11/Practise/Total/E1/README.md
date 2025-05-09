# Apache Flink vs Kafka Streams Performance Comparison

## Mục tiêu
So sánh hiệu suất xử lý dữ liệu giữa Apache Flink và Kafka Streams khi giải quyết cùng một bài toán: Tính tổng doanh thu theo danh mục sản phẩm mỗi giờ.

## Kiến trúc

Dự án này bao gồm:

1. **Tạo dữ liệu mô phỏng**: Tạo ra một tập dữ liệu lớn (>100MB) chứa thông tin về giao dịch bán hàng
2. **Xử lý với Apache Flink**: Sử dụng Flink để tính toán tổng doanh thu theo danh mục sản phẩm mỗi giờ
3. **Xử lý với Kafka Streams**: Sử dụng Kafka để thực hiện cùng một phép tính
4. **So sánh hiệu suất**: Đo và so sánh thời gian xử lý, tài nguyên sử dụng, và độ phức tạp của mã nguồn

## Cấu trúc dự án

```
E1/
├── code/
│   ├── flink/
│   │   └── sales_analysis.py     # Phân tích dữ liệu bằng Apache Flink
│   ├── kafka/
│   │   └── sales_analysis.py     # Phân tích dữ liệu bằng Kafka Streams (Python)
│   ├── generate_sales_data.py    # Tạo dữ liệu mô phỏng
│   ├── run_benchmark.py          # Script chạy benchmark và so sánh
│   └── requirements.txt          # Các thư viện Python cần thiết
├── data/                         # Thư mục chứa dữ liệu và kết quả
│   ├── sales_data.json           # Dữ liệu đầu vào
│   └── results/                  # Kết quả phân tích và so sánh
├── docker-compose.yml            # Cấu hình Docker cho môi trường
└── run.sh                        # Script để chạy toàn bộ hệ thống
```

## Mô tả dữ liệu

Mỗi bản ghi giao dịch bán hàng bao gồm các trường:

- `sale_id`: ID giao dịch
- `customer_id`: ID khách hàng
- `timestamp`: Thời gian giao dịch
- `location`: Địa điểm bán hàng
- `product_category`: Danh mục sản phẩm
- `product_name`: Tên sản phẩm
- `price`: Giá sản phẩm
- `quantity`: Số lượng
- `total_amount`: Tổng số tiền (price * quantity)

## Các bước thực hiện

### 1. Thiết lập môi trường
```bash
chmod +x run.sh
./run.sh
```
Chọn tùy chọn 3 để thiết lập môi trường với Kafka và Flink.

### 2. Tạo dữ liệu mô phỏng
Từ menu, chọn tùy chọn 1 để tạo dữ liệu mô phỏng. Theo mặc định, 1.000.000 bản ghi sẽ được tạo.

### 3. Chạy benchmark so sánh
Từ menu, chọn tùy chọn 2 để chạy cả hai hệ thống và so sánh hiệu suất của chúng.

### 4. Xem kết quả
Kết quả so sánh hiệu suất sẽ được hiển thị và lưu trong thư mục `data/results/`.

## Apache Flink
Flink được triển khai bằng Python sử dụng PyFlink với Table API, tính toán tổng doanh thu theo danh mục sản phẩm trong cửa sổ thời gian 1 giờ.

### Các tính năng chính
- Xử lý theo event time
- Sử dụng cửa sổ thời gian (tumbling window) 1 giờ
- Tổng hợp dữ liệu theo danh mục sản phẩm

## Kafka Streams
Kafka được triển khai bằng Python sử dụng confluent-kafka, thực hiện cùng một phép tính tổng hợp doanh thu theo danh mục và giờ.

### Các tính năng chính
- Sử dụng Producer và Consumer
- Tổng hợp dữ liệu theo danh mục sản phẩm và giờ
- Lưu kết quả vào Kafka topic và file

## Kết quả so sánh
Benchmark sẽ so sánh hai hệ thống dựa trên:
1. Thời gian xử lý
2. Tài nguyên sử dụng
3. Độ phức tạp của mã nguồn

Kết quả sẽ được hiển thị dưới dạng biểu đồ và lưu vào tệp JSON để phân tích thêm.

## Mở rộng
Dự án có thể được mở rộng bằng cách:
1. Thêm các phép tính phức tạp hơn
2. So sánh với các hệ thống xử lý dữ liệu khác
3. Thêm mức độ song song (parallelism) khác nhau
4. Tích hợp với các hệ thống lưu trữ như HDFS, S3
5. Thêm các loại biểu đồ phân tích khác 