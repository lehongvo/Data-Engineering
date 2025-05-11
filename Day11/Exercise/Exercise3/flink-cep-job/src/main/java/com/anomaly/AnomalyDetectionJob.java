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

        DataStream<String> input = env.addSource(consumer);

        // Parse JSON to POJO
        DataStream<Transaction> transactions = input
            .map(json -> new ObjectMapper().readValue(json, Transaction.class))
            .returns(Transaction.class);

        // Key by account_id
        KeyedStream<Transaction, String> keyed = transactions.keyBy(Transaction::getAccountId);

        // Define CEP pattern: 3 giao dịch liên tiếp > 5000 trong 1 phút
        Pattern pattern = Pattern.begin("start")
            .where(new IterativeCondition<Object>() {
                @Override
                public boolean filter(Object t, Context<Object> ctx) {
                    return ((Transaction) t).getAmount() > 5000;
                }
            })
            .next("middle")
            .where(new IterativeCondition<Object>() {
                @Override
                public boolean filter(Object t, Context<Object> ctx) {
                    return ((Transaction) t).getAmount() > 5000;
                }
            })
            .next("end")
            .where(new IterativeCondition<Object>() {
                @Override
                public boolean filter(Object t, Context<Object> ctx) {
                    return ((Transaction) t).getAmount() > 5000;
                }
            })
            .within(Time.minutes(1));

        DataStream<String> alerts = CEP.pattern(keyed, pattern)
            .select((PatternSelectFunction<Transaction, String>) match -> {
                Transaction start = match.get("start").get(0);
                Transaction end = match.get("end").get(0);
                return "Anomaly detected for account " + start.getAccountId() + "!";
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