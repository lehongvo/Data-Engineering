#!/bin/bash

# Bài tập 1: Thiết lập môi trường Kafka và tạo ứng dụng Hello World

# Bước 1: Khởi động Kafka và ZooKeeper
echo "Khởi động Kafka và ZooKeeper..."
docker-compose up -d

# Đợi dịch vụ khởi động hoàn tất
sleep 10
echo "Kafka và ZooKeeper đã khởi động."

# Bước 2: Kiểm tra và tạo topics nếu cần
echo "Kiểm tra và tạo topics..."
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Tạo topics nếu chưa tồn tại (mặc dù đã được cấu hình tự động tạo trong docker-compose.yml)
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic input-topic --partitions 1 --replication-factor 1 --if-not-exists
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic output-topic --partitions 1 --replication-factor 1 --if-not-exists

echo "Topics đã được tạo."

# Bước 3: Tạo thư mục cho ứng dụng Java và tạo các file cần thiết
mkdir -p kafka-streams-app/src/main/java
mkdir -p kafka-streams-app/src/main/resources

# Tạo file pom.xml
cat > kafka-streams-app/pom.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>kafka-streams-app</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <kafka.version>3.5.0</kafka.version>
    </properties>

    <dependencies>
        <!-- Kafka Streams -->
        <dependency>
            <groupId>org.apache.kafka</groupId>
            <artifactId>kafka-streams</artifactId>
            <version>${kafka.version}</version>
        </dependency>
        <!-- SLF4J API -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.36</version>
        </dependency>
        <!-- SLF4J Simple binding -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>1.7.36</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.2.4</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <mainClass>com.example.KafkaStreamsApp</mainClass>
                                </transformer>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
EOF

# Tạo file ứng dụng Java
cat > kafka-streams-app/src/main/java/com/example/KafkaStreamsApp.java << 'EOF'
package com.example;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;
import java.util.concurrent.CountDownLatch;

public class KafkaStreamsApp {

    public static void main(String[] args) {
        // Thiết lập cấu hình cho Kafka Streams
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "uppercase-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

        // Tạo một StreamsBuilder để định nghĩa topology
        StreamsBuilder builder = new StreamsBuilder();

        // Đọc dữ liệu từ input-topic
        KStream<String, String> source = builder.stream("input-topic");

        // Xử lý dữ liệu: chuyển thành chữ HOA
        KStream<String, String> uppercased = source.mapValues(value -> value.toUpperCase());

        // Ghi dữ liệu đã xử lý vào output-topic
        uppercased.to("output-topic");

        // Xây dựng topology
        Topology topology = builder.build();
        System.out.println("Topology: " + topology.describe());

        // Tạo Kafka Streams instance với cấu hình và topology đã định nghĩa
        KafkaStreams streams = new KafkaStreams(topology, props);

        // Xử lý tắt ứng dụng
        CountDownLatch latch = new CountDownLatch(1);
        Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
                System.out.println("Streams application đã đóng");
            }
        });

        try {
            // Khởi động Kafka Streams
            streams.start();
            System.out.println("Streams application đã khởi động");
            latch.await();
        } catch (Exception e) {
            System.exit(1);
        }
    }
}
EOF

# Tạo file properties cho logging
cat > kafka-streams-app/src/main/resources/simplelogger.properties << 'EOF'
org.slf4j.simpleLogger.defaultLogLevel=info
org.slf4j.simpleLogger.showDateTime=true
org.slf4j.simpleLogger.dateTimeFormat=yyyy-MM-dd HH:mm:ss
org.slf4j.simpleLogger.showThreadName=true
EOF

# Bước 4: Biên dịch và đóng gói ứng dụng
echo "Biên dịch và đóng gói ứng dụng..."
cd kafka-streams-app
mvn clean package
cd ..

# Bước 5: Chạy ứng dụng (trong background)
echo "Chạy ứng dụng Kafka Streams..."
java -jar kafka-streams-app/target/kafka-streams-app-1.0-SNAPSHOT.jar &
APP_PID=$!
echo "Ứng dụng đã khởi động với PID: $APP_PID"
sleep 5

# Bước 6: Gửi dữ liệu vào input-topic
echo "Gửi dữ liệu vào input-topic..."
echo "hello world" | docker exec -i kafka kafka-console-producer.sh --bootstrap-server localhost:9092 --topic input-topic
echo "kafka streams" | docker exec -i kafka kafka-console-producer.sh --bootstrap-server localhost:9092 --topic input-topic
echo "đây là bài tập 1" | docker exec -i kafka kafka-console-producer.sh --bootstrap-server localhost:9092 --topic input-topic
sleep 2

# Bước 7: Đọc dữ liệu từ output-topic
echo "Đọc dữ liệu từ output-topic (kết quả):"
docker exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic output-topic --from-beginning --max-messages 3

# Dừng ứng dụng
echo "Dừng ứng dụng Kafka Streams..."
kill $APP_PID
wait $APP_PID 2>/dev/null
echo "Ứng dụng đã dừng."

# Bước 8: Lựa chọn: dừng Kafka và ZooKeeper sau khi hoàn thành
read -p "Bạn có muốn dừng Kafka và ZooKeeper không? (y/n): " choice
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
    echo "Dừng Kafka và ZooKeeper..."
    docker-compose down
    echo "Kafka và ZooKeeper đã dừng."
fi

echo "Bài tập 1 đã hoàn thành!"