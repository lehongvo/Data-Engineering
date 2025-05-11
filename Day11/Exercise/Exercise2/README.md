# Exercise 2: Kafka Avro Schema Management

## Mục tiêu
- Quản lý schema với Avro cho Kafka producer/consumer
- Thiết kế schema Avro
- Cấu hình Schema Registry
- Producer gửi dữ liệu Avro
- Consumer đọc dữ liệu Avro
- Xử lý schema evolution
- Kiểm tra tính tương thích schema

## Cấu trúc thư mục
```
Exercise2/
  ├── code/
  │     ├── producer_avro.py
  │     └── consumer_avro.py
  ├── schema/
  │     └── user.avsc
  ├── config/
  ├── data/
  ├── requirements.txt
  ├── docker-compose.yml
  └── README.md
```

## Hướng dẫn chạy

### 1. Khởi động Kafka, Zookeeper, Schema Registry
```bash
docker-compose up -d
```

### 2. Cài đặt thư viện Python
```bash
pip install -r requirements.txt
```

### 3. Chạy producer gửi dữ liệu Avro
```bash
python code/producer_avro.py
```

### 4. Chạy consumer đọc dữ liệu Avro
```bash
python code/consumer_avro.py
```

## Schema Avro mẫu
File: `schema/user.avsc`
```json
{
  "namespace": "example.avro",
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "int"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

## Schema Evolution
- Để kiểm tra schema evolution, hãy thử sửa file `user.avsc` (ví dụ: thêm field mới với default value) và chạy lại producer.
- Kiểm tra consumer có đọc được dữ liệu mới không.
- Có thể kiểm tra schema và compatibility tại: http://localhost:8081

## Tham khảo
- [Confluent Schema Registry Docs](https://docs.confluent.io/platform/current/schema-registry/index.html)
- [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
