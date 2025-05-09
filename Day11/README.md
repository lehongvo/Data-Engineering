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

## Bài Tập Thực Hành Đơn Giản

### Bài tập về Apache Kafka Streams

#### Bài tập 1: Thiết lập môi trường Kafka và tạo ứng dụng Hello World
- **Mục tiêu**: Làm quen với cú pháp và cài đặt Kafka Streams
- **Yêu cầu**:
  1. Cài đặt Kafka trên máy local
  2. Tạo 2 topics: "input-topic" và "output-topic"
  3. Viết ứng dụng Kafka Streams đơn giản để đọc chuỗi từ input-topic, chuyển thành chữ HOA và ghi vào output-topic
  4. Kiểm tra kết quả bằng console consumer

#### Bài tập 2: Xử lý dữ liệu nhiệt độ
- **Mục tiêu**: Thực hành với windowing và aggregations
- **Yêu cầu**:
  1. Tạo producer giả lập dữ liệu nhiệt độ từ các cảm biến (sensorId, temperature, timestamp)
  2. Viết ứng dụng Kafka Streams để:
     - Tính nhiệt độ trung bình theo cửa sổ thời gian 5 phút
     - Phát hiện cảm biến có nhiệt độ cao bất thường (> 30°C)
     - Ghi kết quả vào các topics khác nhau

#### Bài tập 3: Join và Enrichment
- **Mục tiêu**: Thực hành KStream-KTable join
- **Yêu cầu**:
  1. Tạo topic "user-clicks" chứa thông tin (userId, pageId, timestamp)
  2. Tạo topic "user-profiles" chứa thông tin (userId, name, region)
  3. Viết ứng dụng Kafka Streams để join hai streams và tạo ra dữ liệu làm giàu có dạng (name, region, pageId, timestamp)
  4. Tính số lần click theo region sử dụng cửa sổ thời gian 1 giờ

### Bài tập về Apache Flink

#### Bài tập 1: WordCount với Flink
- **Mục tiêu**: Làm quen với cú pháp cơ bản của Flink
- **Yêu cầu**:
  1. Thiết lập môi trường Flink
  2. Đọc dữ liệu từ file văn bản
  3. Tính số lần xuất hiện của mỗi từ
  4. In kết quả ra màn hình hoặc lưu vào file

#### Bài tập 2: Phân tích dữ liệu truy cập web
- **Mục tiêu**: Thực hành windowing, filtering và aggregations
- **Yêu cầu**:
  1. Tạo dataset mô phỏng dữ liệu log truy cập web (ip, URL, timestamp, status code)
  2. Viết ứng dụng Flink để:
     - Lọc các requests lỗi (status code >= 400)
     - Tính số lượng truy cập theo URL trong cửa sổ thời gian 10 phút
     - Phát hiện các địa chỉ IP có số lượng requests lỗi bất thường

#### Bài tập 3: Phân tích dữ liệu giao dịch theo thời gian thực
- **Mục tiêu**: Thực hành event time processing và watermarks
- **Yêu cầu**:
  1. Tạo dataset mô phỏng dữ liệu giao dịch (transactionId, customerId, amount, timestamp)
  2. Viết ứng dụng Flink để:
     - Xử lý dữ liệu theo event time với watermarks
     - Tính tổng số tiền giao dịch theo khách hàng trong cửa sổ trượt 30 phút
     - Phát hiện các giao dịch có giá trị cao bất thường (> $1000)

### Bài tập kết hợp (nâng cao)

#### Bài tập 1: So sánh hiệu suất
- **Mục tiêu**: So sánh Kafka Streams và Flink trên cùng một bài toán
- **Yêu cầu**:
  1. Tạo dataset đủ lớn (>100MB) chứa dữ liệu bán hàng
  2. Giải quyết cùng một bài toán (tính tổng doanh thu theo danh mục sản phẩm mỗi giờ) bằng cả Kafka Streams và Flink
  3. Đo và so sánh thời gian xử lý, tài nguyên sử dụng, độ phức tạp của mã nguồn

#### Bài tập 2: Xây dựng pipeline ETL đơn giản
- **Mục tiêu**: Áp dụng kiến thức vào một pipeline ETL thực tế
- **Yêu cầu**:
  1. Thu thập dữ liệu từ một API public (như Twitter API hoặc Weather API)
  2. Xử lý và làm sạch dữ liệu sử dụng Kafka Streams hoặc Flink
  3. Lưu dữ liệu đã xử lý vào cơ sở dữ liệu (MySQL, MongoDB, etc.)
  4. Tạo dashboard đơn giản để hiển thị kết quả

## Hướng dẫn nộp bài
1. Tạo một GitHub repository cho mỗi bài tập
2. Mỗi repository phải chứa:
   - Mã nguồn đầy đủ
   - File README mô tả cách chạy ứng dụng
   - Tài liệu giải thích cách tiếp cận và kết quả đạt được
3. Demo ứng dụng bằng screencast nếu có thể

Chúc bạn học tập vui vẻ và hiệu quả!