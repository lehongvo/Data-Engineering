# Ethereum Blockchain Real-time Data Processing với Kafka

Hệ thống xử lý dữ liệu blockchain Ethereum theo thời gian thực, sử dụng Apache Kafka.

## Thành phần chính

1. **Tạo và quản lý topics** - Thiết lập cấu trúc topics cho dữ liệu blockchain
2. **Producer** - Thu thập dữ liệu từ Ethereum blockchain và gửi đến Kafka
3. **Consumer** - Nhận và xử lý dữ liệu từ Kafka
4. **Kafka Streams** - Xử lý luồng dữ liệu theo thời gian thực

## Cài đặt

Cách đơn giản nhất là sử dụng script `run.sh`:

```bash
# Cài đặt môi trường (kiểm tra phụ thuộc, cài đặt thư viện Python và tạo file .env)
./run.sh setup

# HOẶC chạy trực tiếp tất cả các thành phần (bao gồm cài đặt thư viện)
./run.sh start-all
```

Script sẽ tự động:
1. Kiểm tra Python và pip
2. Cài đặt các thư viện từ requirements.txt
3. Kiểm tra Docker
4. Tạo file .env với cấu hình mặc định
5. Tạo và quản lý Kafka topics

## Sử dụng với run.sh

Script `run.sh` cung cấp các lệnh để quản lý hệ thống dễ dàng:

```bash
# Chỉ cài đặt các thư viện Python
./run.sh install

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