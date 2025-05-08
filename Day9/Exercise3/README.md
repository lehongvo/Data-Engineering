# Exercise 3: Consumer Groups và Phân phối dữ liệu trong Kafka

## Mô tả
Bài tập này minh họa cách Kafka phân phối dữ liệu đến các Consumer Group khác nhau để xử lý song song và độc lập. Hệ thống mô phỏng:

1. **Producer** tạo dữ liệu giao dịch thương mại điện tử với các trường: user_id, product_id, amount, timestamp
2. **Consumer Group 1** (Revenue Aggregator): tổng hợp doanh thu theo sản phẩm
3. **Consumer Group 2** (User Behavior Analyzer): phân tích hành vi người dùng và xác định khách hàng giá trị cao

## Yêu cầu
- Kafka chạy trên `localhost:9092`
- Python 3 với thư viện `kafka-python`

Cài đặt thư viện:
```bash
pip install kafka-python
```

## Cách chạy

### Phương pháp 1: Sử dụng script tự động
```bash
chmod +x run.sh
./run.sh
```

### Phương pháp 2: Chạy từng thành phần riêng biệt
#### Terminal 1: Khởi động Kafka (nếu chưa chạy)
```bash
docker-compose up -d
```

#### Terminal 2: Chạy Consumer Group 1 (Tổng hợp doanh thu)
```bash
python3 consumer_group1.py
```

#### Terminal 3: Chạy Consumer Group 2 (Phân tích người dùng)
```bash
python3 consumer_group2.py
```

#### Terminal 4: Chạy Producer
```bash
python3 transaction_producer.py
```

## Kết quả mong đợi
1. **Transaction Producer** sẽ tạo các giao dịch thương mại ngẫu nhiên và liên tục
2. **Consumer Group 1** sẽ:
   - Tính tổng doanh thu từng sản phẩm
   - Hiển thị các sản phẩm theo thứ tự doanh thu
   - Tính tổng số lượng đơn hàng từng sản phẩm
3. **Consumer Group 2** sẽ:
   - Phân tích hành vi của người dùng
   - Xác định và theo dõi khách hàng giá trị cao
   - Hiển thị top 5 khách hàng theo chi tiêu

## Điểm quan trọng
- Cả hai Consumer Group đều nhận được tất cả dữ liệu từ Producer
- Mỗi Consumer Group xử lý dữ liệu độc lập theo cách riêng
- Kafka đảm bảo cả hai Consumer Group nhận được tất cả dữ liệu
- Mỗi nhóm có thể xử lý dữ liệu ở tốc độ riêng mà không ảnh hưởng đến nhóm khác

## Ghi chú
- Nhấn `Ctrl+C` để dừng các tiến trình
- Xem log của từng component trong file `transaction_producer.log`, `consumer_group1.log`, `consumer_group2.log` 