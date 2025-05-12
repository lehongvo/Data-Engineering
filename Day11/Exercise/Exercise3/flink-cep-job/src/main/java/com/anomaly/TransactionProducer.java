package com.anomaly;

import java.util.Properties;
import java.util.Random;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import com.fasterxml.jackson.databind.ObjectMapper;

public class TransactionProducer {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9097");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);
        ObjectMapper mapper = new ObjectMapper();
        Random random = new Random();

        try {
            // Tạo ra 10 giao dịch thông thường
            for (int i = 0; i < 10; i++) {
                Transaction transaction = new Transaction();
                transaction.setTransactionId("tx-" + random.nextInt(1000));
                transaction.setAccountId("acc-" + random.nextInt(10));
                transaction.setAmount(random.nextDouble() * 3000); // Số tiền nhỏ hơn 3000

                String json = mapper.writeValueAsString(transaction);
                producer.send(new ProducerRecord<>("transactions", json));
                System.out.println("Sent: " + json);
                Thread.sleep(1000);
            }
            
            // Tạo ra 3 giao dịch liên tiếp từ cùng 1 tài khoản với số tiền > 3000
            for (int i = 0; i < 3; i++) {
                Transaction transaction = new Transaction();
                transaction.setTransactionId("tx-special-" + i);
                transaction.setAccountId("acc-special");
                transaction.setAmount(5000 + i * 1000); // Số tiền > 3000

                String json = mapper.writeValueAsString(transaction);
                producer.send(new ProducerRecord<>("transactions", json));
                System.out.println("Sent SPECIAL: " + json);
                Thread.sleep(1000);
            }
            
            // Tiếp tục giao dịch thông thường
            while (true) {
                Transaction transaction = new Transaction();
                transaction.setTransactionId("tx-" + random.nextInt(1000));
                transaction.setAccountId("acc-" + random.nextInt(10));
                transaction.setAmount(random.nextDouble() * 10000);

                String json = mapper.writeValueAsString(transaction);
                producer.send(new ProducerRecord<>("transactions", json));
                System.out.println("Sent: " + json);
                Thread.sleep(1000);
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            producer.close();
        }
    }
} 