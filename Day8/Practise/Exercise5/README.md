# Exercise 5: Real-Time Analytics with Kafka and Spark Streaming

## 1. Event Collection (Kafka Setup)
- Set up a Kafka cluster (can use local single-node for practice).
- Create topics for user events: `page_views`, `clicks`, `add_to_cart`, `purchases`.
- Use Kafka producer to simulate user events (can use Python, Node.js, or Kafka CLI).

## 2. Real-Time Processing with Spark Streaming
- Use PySpark's Structured Streaming to consume data from Kafka topics.
- Parse incoming events (JSON format recommended).
- Compute real-time KPIs using sliding window (e.g., number of page views, conversion rate, etc.).
- Detect abnormal behaviors (e.g., too many clicks in a short time from one user) and generate alerts.
- Ensure the streaming job is fault-tolerant and scalable (checkpointing, parallelism).

## 3. Storage and Visualization
- Store processed results and alerts into Elasticsearch.
- Set up Kibana to visualize KPIs and alerts in real time (create dashboards, charts, etc.).

## 4. Step-by-Step Guide

### 4.1. Kafka Setup
- Install Kafka (local or Docker).
- Start Zookeeper and Kafka broker.
- Create required topics:
  ```sh
  kafka-topics.sh --create --topic page_views --bootstrap-server localhost:9092
  kafka-topics.sh --create --topic clicks --bootstrap-server localhost:9092
  kafka-topics.sh --create --topic add_to_cart --bootstrap-server localhost:9092
  kafka-topics.sh --create --topic purchases --bootstrap-server localhost:9092
  ```
- Use a producer to send sample events (can use `kafka-console-producer.sh` or a custom script).

### 4.2. Spark Streaming
- Install PySpark and required dependencies:
  ```sh
  pip install pyspark kafka-python elasticsearch
  ```
- Write a PySpark Structured Streaming job to:
  - Read from Kafka topics
  - Parse JSON events
  - Compute sliding window aggregations
  - Detect anomalies and generate alerts
  - Write results to Elasticsearch

### 4.3. Elasticsearch & Kibana
- Install Elasticsearch and Kibana (local or Docker).
- Configure Elasticsearch index for results and alerts.
- Use Kibana to create dashboards for real-time monitoring.

## 5. References
- [Kafka Quickstart](https://kafka.apache.org/quickstart)
- [PySpark Structured Streaming + Kafka](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
- [Elasticsearch Python Client](https://elasticsearch-py.readthedocs.io/en/latest/)
- [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html)

---

**Tips:**
- Use Docker Compose for quick setup of Kafka, Elasticsearch, and Kibana.
- Always test with sample data before going to production.
- Monitor Spark Streaming job for latency and throughput. 