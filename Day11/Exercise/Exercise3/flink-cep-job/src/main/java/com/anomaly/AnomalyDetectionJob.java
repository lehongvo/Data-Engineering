package com.anomaly;

import java.util.Properties;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.PatternSelectFunction;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.KeyedStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;

import com.fasterxml.jackson.databind.ObjectMapper;

public class AnomalyDetectionJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "localhost:9097");
        properties.setProperty("group.id", "flink-cep");

        FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
                "transactions",
                new SimpleStringSchema(),
                properties
        );

        // Bắt đầu từ các sự kiện mới
        consumer.setStartFromLatest();

        DataStream<String> input = env.addSource(consumer);

        // Parse JSON to POJO
        DataStream<Transaction> transactions = input
            .map(json -> {
                Transaction t = new ObjectMapper().readValue(json, Transaction.class);
                System.out.println("Processing transaction: " + json);
                return t;
            })
            .returns(Transaction.class);

        // Key by account_id
        KeyedStream<Transaction, String> keyed = transactions.keyBy(Transaction::getAccountId);

        // Define CEP pattern: 3 giao dịch liên tiếp > 3000 trong 1 phút
        Pattern<Transaction, ?> pattern = Pattern.<Transaction>begin("start")
            .where(new IterativeCondition<Transaction>() {
                @Override
                public boolean filter(Transaction t, Context<Transaction> ctx) {
                    System.out.println("Checking start condition for: " + t.getAccountId() + " - " + t.getAmount());
                    return t.getAmount() > 3000;
                }
            })
            .next("middle")
            .where(new IterativeCondition<Transaction>() {
                @Override
                public boolean filter(Transaction t, Context<Transaction> ctx) {
                    System.out.println("Checking middle condition for: " + t.getAccountId() + " - " + t.getAmount());
                    return t.getAmount() > 3000;
                }
            })
            .next("end")
            .where(new IterativeCondition<Transaction>() {
                @Override
                public boolean filter(Transaction t, Context<Transaction> ctx) {
                    System.out.println("Checking end condition for: " + t.getAccountId() + " - " + t.getAmount());
                    return t.getAmount() > 3000;
                }
            })
            .within(Time.minutes(1));

        DataStream<String> alerts = CEP.pattern(keyed, pattern)
            .select((PatternSelectFunction<Transaction, String>) match -> {
                Transaction start = match.get("start").get(0);
                Transaction middle = match.get("middle").get(0);
                Transaction end = match.get("end").get(0);
                String alert = "ANOMALY DETECTED for account " + start.getAccountId() + 
                        "! Transactions: " + start.getTransactionId() + 
                        ", " + middle.getTransactionId() + 
                        ", " + end.getTransactionId();
                System.out.println(">>> " + alert);
                return alert;
            });

        // Gửi cảnh báo ra Kafka topic 'anomaly-alerts'
        FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(
            "anomaly-alerts",
            new SimpleStringSchema(),
            properties
        );
        alerts.addSink(kafkaProducer);
        alerts.print();
        env.execute("Flink CEP Anomaly Detection");
    }
} 