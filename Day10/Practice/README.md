# Ethereum Blockchain Real-time Data Processing với Kafka

Hệ thống xử lý dữ liệu blockchain Ethereum theo thời gian thực, sử dụng Apache Kafka.

## Thành phần chính

1. **Tạo và quản lý topics** - Thiết lập cấu trúc topics cho dữ liệu blockchain
2. **Producer** - Thu thập dữ liệu từ Ethereum blockchain và gửi đến Kafka
3. **Consumer** - Nhận và xử lý dữ liệu từ Kafka
4. **Kafka Streams** - Xử lý luồng dữ liệu theo thời gian thực

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```
pip install -r requirements.txt
```

2. Sử dụng script `run.sh` để cài đặt và chạy hệ thống:
```
# Kiểm tra môi trường và tạo file .env
./run.sh setup
```

3. Hoặc chạy Kafka và Zookeeper thủ công (yêu cầu Docker):
```
docker-compose up -d
```

## Sử dụng với run.sh

Script `run.sh` cung cấp các lệnh để quản lý hệ thống dễ dàng:

```
# Khởi động Kafka và Zookeeper
./run.sh start-kafka

# Tạo Kafka topics
./run.sh create-topics

# Chạy từng thành phần riêng biệt
./run.sh producer
./run.sh consumer
./run.sh streams

# Khởi động tất cả (Kafka + tất cả thành phần)
./run.sh start-all

# Dừng tất cả
./run.sh stop-all

# Xem trợ giúp
./run.sh help
```

## Sử dụng thủ công

1. Khởi tạo topics:
```
python kafka_admin.py
```

2. Chạy producer để thu thập dữ liệu blockchain:
```
python eth_producer.py
```

3. Chạy consumer để xử lý dữ liệu:
```
python eth_consumer.py
```

4. (Tùy chọn) Chạy ứng dụng Kafka Streams:
```
python eth_streams.py
```

## Cấu hình

Bạn có thể tùy chỉnh các cài đặt trong file `config.yml`:

- **Kafka topics**: Thay đổi tên và cấu hình của các topics
- **Ethereum providers**: Cấu hình kết nối đến Ethereum node
- **Ngưỡng xử lý**: Thay đổi ngưỡng để xác định giao dịch giá trị cao

## Ethereum RPC Provider

Hệ thống này sử dụng [Llama RPC](https://eth.llamarpc.com) làm nhà cung cấp RPC mặc định cho Ethereum, giúp bạn không cần đăng ký API key với Infura hoặc Alchemy. Bạn có thể thay đổi nhà cung cấp trong file `config.yml` hoặc thông qua biến môi trường `ETH_PROVIDER_URL`.

## Môi trường

File `.env` mặc định:

```
# Direct provider URL - Using LlamaRPC public endpoint
ETH_PROVIDER_URL=https://eth.llamarpc.com

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
``` 