#!/bin/bash

# Khởi động Kafka và Zookeeper bằng docker-compose nếu chưa chạy
if ! docker ps --format '{{.Names}}' | grep -q 'kafka'; then
  echo "Đang khởi động Kafka và Zookeeper bằng docker-compose..."
  docker-compose down 2>/dev/null
  docker-compose up -d
  echo "Đợi Kafka broker khởi động (20 giây)..."
  sleep 5
else
  echo "Kafka và Zookeeper đã chạy..."
fi

# Kiểm tra và cài đặt kafka-python nếu chưa có
python3 -c "import kafka" 2>/dev/null || pip3 install kafka-python

# Hướng dẫn sử dụng
cat << EOF
============================
Chạy Kafka Consumer & Producer
============================
- Consumer sẽ chạy ở background (log lưu vào consumer.log)
- Producer sẽ chạy ở foreground
- Để dừng, nhấn Ctrl+C
============================
EOF

# Chạy consumer ở background
python3 consumer.py > consumer.log 2>&1 &
CONSUMER_PID=$!
echo "Consumer đang chạy (PID: $CONSUMER_PID), log: consumer.log"

# Chạy producer ở foreground
python3 producer.py > producer.log 2>&1 &
PRODUCER_PID=$!
echo "Producer đang chạy (PID: $PRODUCER_PID), log: producer.log"

# Hiển thị log producer (có thể dừng bằng Ctrl+C)
echo "Đang hiển thị producer.log (Ctrl+C để dừng)..."
tail -f producer.log

# Khi producer dừng, dừng luôn consumer
kill $CONSUMER_PID
wait $CONSUMER_PID 2>/dev/null 