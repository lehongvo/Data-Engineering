# Exercise 4: Kafka Connect - Tích hợp với nguồn dữ liệu bên ngoài

## Giới thiệu

Kafka Connect là một framework mạnh mẽ và mở rộng được thiết kế để kết nối Apache Kafka với các nguồn dữ liệu bên ngoài như cơ sở dữ liệu, hệ thống tập tin, dịch vụ đám mây, và các ứng dụng khác. Nó cung cấp một cách tiêu chuẩn để đưa dữ liệu vào và ra khỏi Kafka, giúp xây dựng các pipeline dữ liệu theo thời gian thực.

## Các khái niệm chính

### 1. Source Connector và Sink Connector
- **Source Connector**: Đọc dữ liệu từ các hệ thống ngoài và ghi vào Kafka topic
- **Sink Connector**: Đọc dữ liệu từ Kafka topic và ghi ra các hệ thống ngoài

### 2. Deployment Mode
- **Standalone Mode**: Chạy trên máy chủ đơn lẻ
- **Distributed Mode**: Chạy trên cụm Kafka, có khả năng mở rộng và fault-tolerant

### 3. Transformations
- Cho phép biến đổi dữ liệu khi nó di chuyển qua pipeline

## Bài tập

Trong bài tập này, chúng ta sẽ thiết lập một pipeline hoàn chỉnh sử dụng Kafka Connect để:

1. **Source Connector với PostgreSQL**: Đọc dữ liệu từ PostgreSQL và đưa vào Kafka
2. **Sink Connector đến MongoDB**: Đọc dữ liệu từ Kafka và ghi vào MongoDB

## Yêu cầu
- Docker và Docker Compose
- Hiểu biết cơ bản về Kafka, PostgreSQL và MongoDB

## Hướng dẫn triển khai

### 1. Cài đặt và cấu hình

- **Docker Compose File**: Chứa cấu hình cho Zookeeper, Kafka, Kafka Connect, PostgreSQL, và MongoDB
- **Connector Configuration Files**:
  - `connect-standalone.properties`: Cấu hình chung cho Kafka Connect
  - `postgres-source.properties`: Cấu hình cho Source Connector
  - `mongodb-sink.properties`: Cấu hình cho Sink Connector

### 2. Chạy môi trường Kafka Connect

```bash
chmod +x run.sh
./run.sh
```

### 3. Kiểm tra luồng dữ liệu

1. Dữ liệu ban đầu được tải vào PostgreSQL từ file `init.sql`
2. Kafka Connect source sẽ đọc dữ liệu từ PostgreSQL và gửi đến Kafka topics
3. Kafka Connect sink sẽ đọc dữ liệu từ Kafka topics và ghi vào MongoDB

### 4. Theo dõi và test

Sau khi hệ thống đã chạy, bạn có thể:

1. Xem danh sách các Kafka topics:
```bash
docker-compose exec kafka kafka-topics.sh --list --bootstrap-server kafka:9092
```

2. Kiểm tra dữ liệu trong PostgreSQL:
```bash
docker-compose exec postgres psql -U postgres -d kafkaconnect -c 'SELECT * FROM customers;'
```

3. Kiểm tra dữ liệu trong MongoDB:
```bash
docker-compose exec mongodb mongosh --username root --password example --authenticationDatabase admin kafkaconnect --eval 'db.customers.find()'
```

4. Thêm dữ liệu mới vào PostgreSQL và xem nó tự động cập nhật trong MongoDB:
```bash
docker-compose exec postgres psql -U postgres -d kafkaconnect -c "INSERT INTO customers (name, email) VALUES ('New Customer', 'new.customer@example.com');"
```

## Ứng dụng thực tế

1. **CDC (Change Data Capture)**: Bắt các thay đổi từ cơ sở dữ liệu và gửi đến các hệ thống khác
2. **Data Lake Integration**: Tự động đưa dữ liệu từ nhiều nguồn vào data lake
3. **ETL theo thời gian thực**: Xây dựng pipeline ETL có độ trễ thấp
4. **Microservices Integration**: Tích hợp giữa các microservices thông qua Kafka

## Lợi ích của Kafka Connect

1. **Declarative Configuration**: Cấu hình dựa trên file properties
2. **Scalability**: Khả năng mở rộng quy mô theo nhu cầu
3. **Reliability**: Xử lý lỗi và đảm bảo giao dịch
4. **Ecosystem**: Nhiều connector đã được xây dựng sẵn cho các hệ thống phổ biến
5. **Monitoring**: Tích hợp với các công cụ giám sát Kafka

## Tài liệu tham khảo
- [Kafka Connect Documentation](https://kafka.apache.org/documentation/#connect)
- [Debezium PostgreSQL Connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
- [MongoDB Kafka Connector](https://www.mongodb.com/docs/kafka-connector/current/)

## Ghi chú
- Trong môi trường sản xuất, bạn sẽ muốn chạy Kafka Connect ở chế độ distributed để có khả năng mở rộng và chịu lỗi tốt hơn.
- Theo dõi log của Kafka Connect để gỡ lỗi: `docker-compose logs -f kafka-connect` 