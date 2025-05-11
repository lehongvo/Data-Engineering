#!/bin/bash

# Kiểm tra xem Docker và docker-compose đã được cài đặt chưa
if ! command -v docker &> /dev/null; then
    echo "Docker chưa được cài đặt. Vui lòng cài đặt trước."
    exit 1
fi

# Khởi động lại Kafka với docker-compose
echo "Khởi động Kafka..."
docker-compose down
docker-compose up -d
echo "Đợi Kafka khởi động hoàn tất (15 giây)..."
sleep 15

# Tạo các topic nếu chưa tồn tại
echo "Tạo topic transactions..."
docker exec kafka kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9097 \
    --topic transactions \
    --partitions 1 \
    --replication-factor 1

echo "Tạo topic anomaly-alerts..."
docker exec kafka kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9097 \
    --topic anomaly-alerts \
    --partitions 1 \
    --replication-factor 1

# Build project
echo "Build project..."
mvn clean package

# Chạy producer và consumer trong các cửa sổ terminal riêng biệt
echo "Chạy TransactionProducer để gửi dữ liệu vào Kafka..."
java -cp target/flink-cep-job-1.0-SNAPSHOT.jar com.anomaly.TransactionProducer &
PRODUCER_PID=$!

# Chạy anomaly detection job
echo "Chạy AnomalyDetectionJob để phát hiện giao dịch bất thường..."
java -cp target/flink-cep-job-1.0-SNAPSHOT.jar com.anomaly.AnomalyDetectionJob &
DETECTION_PID=$!

# Theo dõi topic anomaly-alerts
echo "Theo dõi các cảnh báo giao dịch bất thường từ topic anomaly-alerts..."
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9097 --topic anomaly-alerts --from-beginning

# Xử lý khi người dùng nhấn Ctrl+C
trap 'kill $PRODUCER_PID $DETECTION_PID; echo "Đã dừng tất cả các tiến trình."; exit' INT

# Chờ các tiến trình con hoàn thành
wait
