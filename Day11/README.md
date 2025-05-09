# Học Về Xử Lý Dữ Liệu Thời Gian Thực

Ngày cập nhật: 9 Tháng 5, 2025

## Apache Kafka Streams

### Giới thiệu
Apache Kafka Streams là một thư viện client để xử lý và phân tích dữ liệu lưu trữ trong Kafka. Nó cho phép xây dựng các ứng dụng và microservices xử lý dữ liệu theo thời gian thực, với tính năng trạng thái, tính chịu lỗi, và khả năng mở rộng.

### Các khái niệm cơ bản
- **Stream**: Luồng dữ liệu liên tục, không giới hạn
- **Stream Processing**: Xử lý từng sự kiện/dữ liệu đến liên tục, theo thời gian thực
- **Stateless Processing**: Xử lý không lưu trạng thái (filter, map)
- **Stateful Processing**: Xử lý có lưu trạng thái (aggregations, windowing)

### Kiến trúc Kafka Streams
- **Topology**: Đồ thị có hướng của các stream processors
- **Source Processor**: Đọc dữ liệu từ Kafka topic
- **Processor Node**: Xử lý dữ liệu
- **Sink Processor**: Ghi dữ liệu vào Kafka topic

### Các API chính
1. **Streams DSL**: API cấp cao dựa trên các stream và table
   - `KStream`: Đại diện cho stream dữ liệu liên tục
   - `KTable`: Đại diện cho stream với update log-compacted
   - `GlobalKTable`: Phiên bản của KTable có sao chép đến tất cả instances

2. **Processor API**: API cấp thấp hơn để kiểm soát nhiều hơn

### Ví dụ đơn giản
```java
StreamsBuilder builder = new StreamsBuilder();
KStream<String, String> textLines = builder.stream("input-topic");

// Xử lý dữ liệu: đếm số từ
KTable<String, Long> wordCounts = textLines
    .flatMapValues(line -> Arrays.asList(line.toLowerCase().split("\\W+")))
    .groupBy((key, word) -> word)
    .count();

// Ghi kết quả vào topic khác
wordCounts.toStream().to("output-topic", Produced.with(Serdes.String(), Serdes.Long()));
```

### Cách thiết lập ứng dụng Kafka Streams
1. Thêm dependency:
```xml
<!-- Maven -->
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-streams</artifactId>
    <version>3.5.0</version>
</dependency>
```

2. Thiết lập cấu hình:
```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "my-stream-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
```

## Apache Flink Basics

### Giới thiệu
Apache Flink là một framework và distributed processing engine cho việc xử lý dữ liệu stateful stream và batch processing. Flink được thiết kế để chạy trong tất cả các môi trường cluster phổ biến, thực hiện tính toán với tốc độ trong bộ nhớ và quy mô bất kỳ.

### Kiến trúc Flink
- **Client**: Chuẩn bị và gửi chương trình tới JobManager
- **JobManager**: Điều phối thực thi, quản lý checkpoint và recovery
- **TaskManager**: Thực thi các tasks của job, trao đổi dữ liệu với TaskManagers khác

### Các khái niệm cơ bản
- **DataStream API**: Xử lý dữ liệu có giới hạn hoặc không giới hạn
- **DataSet API**: Xử lý dữ liệu có giới hạn (batch processing)
- **Table API & SQL**: API quan hệ có cấu trúc cao hơn

### Các tính năng chính
1. **Event Time Processing**: Xử lý sự kiện dựa trên thời gian tạo ra, không phải thời gian nhận
2. **State Management**: Quản lý trạng thái có khả năng mở rộng và chịu lỗi
3. **Checkpointing**: Cơ chế để đảm bảo exactly-once processing
4. **Windowing**: Chia dữ liệu thành "cửa sổ" thời gian để xử lý

### Ví dụ DataStream API
```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Tạo DataStream từ nguồn dữ liệu
DataStream<String> text = env.readTextFile("input.txt");

// Xử lý dữ liệu
DataStream<Tuple2<String, Integer>> wordCounts = text
    .flatMap(new Tokenizer())
    .keyBy(value -> value.f0)
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
    .sum(1);

// In kết quả hoặc gửi tới sink
wordCounts.print();

// Thực thi job
env.execute("Word Count Example");
```

### Cách thiết lập ứng dụng Flink
1. Thêm dependency:
```xml
<!-- Maven -->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-streaming-java</artifactId>
    <version>1.18.0</version>
</dependency>
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-clients</artifactId>
    <version>1.18.0</version>
</dependency>
```

2. Code cơ bản:
```java
public class StreamingJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Thêm source, transformations và sinks
        
        env.execute("My Flink Job");
    }
}
```

## So sánh Kafka Streams và Flink

| Tính năng | Kafka Streams | Apache Flink |
|-----------|---------------|--------------|
| Kiến trúc | Thư viện (không có server) | Distributed framework |
| Cài đặt | Đơn giản (chỉ là thư viện) | Phức tạp hơn (cluster) |
| Tích hợp | Chỉ với Kafka | Nhiều nguồn dữ liệu |
| Quy mô | Nhỏ đến trung bình | Từ nhỏ đến cực lớn |
| Use case | Xử lý stream đơn giản | Xử lý stream phức tạp |

## Tài nguyên học tập

### Kafka Streams
- [Tài liệu chính thức](https://kafka.apache.org/documentation/streams/)
- [Kafka Streams in Action (sách)](https://www.manning.com/books/kafka-streams-in-action)
- [Confluent's Kafka Tutorial](https://www.confluent.io/blog/tag/kafka-streams/)

### Apache Flink
- [Tài liệu chính thức](https://flink.apache.org/docs/stable/)
- [Flink Training](https://training.ververica.com/)
- [Stream Processing with Apache Flink (sách)](https://www.oreilly.com/library/view/stream-processing-with/9781491974285/)

## Dự án thực hành

1. **Bắt đầu với Kafka Streams**:
   - Xây dựng ứng dụng theo dõi lượt truy cập trang web theo thời gian thực
   - Tạo hệ thống phát hiện gian lận đơn giản

2. **Bắt đầu với Flink**:
   - Phân tích dữ liệu cảm biến IoT theo thời gian thực
   - Xây dựng dashboard phân tích xu hướng mạng xã hội

Chúc bạn học tập hiệu quả!