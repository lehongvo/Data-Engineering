# Exercise 1: Kafka Producer & Consumer (Gửi và nhận dữ liệu cảm biến)

## Mô tả
Bài tập này giúp bạn thực hành tạo một producer và một consumer sử dụng Apache Kafka để gửi và nhận dữ liệu cảm biến (sensor data) theo thời gian thực.

## Yêu cầu
- Đã cài đặt Kafka và đang chạy trên `localhost:9092`
- Đã cài đặt Python và thư viện `kafka-python`

Cài đặt thư viện:
```bash
pip install kafka-python
```

## Cách chạy
### 1. Chạy Consumer trước để nhận dữ liệu:
```bash
python consumer.py
```

### 2. Mở terminal khác, chạy Producer để gửi dữ liệu:
```bash
python producer.py
```

## Kết quả mong đợi
- Terminal consumer sẽ hiển thị các bản ghi dữ liệu cảm biến nhận được từ producer theo thời gian thực.
- Terminal producer sẽ hiển thị các bản ghi đã gửi.

## Ghi chú
- Để dừng chương trình, nhấn `Ctrl+C`.
- Có thể chỉnh sửa logic sinh dữ liệu trong file `producer.py` cho phù hợp với bài toán thực tế. 