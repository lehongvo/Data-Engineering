# Exercise 5: Real-Time Analytics with Kafka and Spark Streaming
# Requirements: pyspark, kafka-python, elasticsearch
# Install: pip install pyspark kafka-python elasticsearch

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from elasticsearch import Elasticsearch
import json

# Define schema for incoming events (example: page view event)
event_schema = StructType([
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("page", StringType()),
    StructField("product_id", StringType()),
])

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingExercise5") \
    .getOrCreate()

# Read stream from Kafka (example topic: page_views)
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "page_views"

df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "latest") \
    .load()

# Parse value as JSON
df_parsed = df_raw.select(from_json(col("value").cast("string"), event_schema).alias("data")).select("data.*")

# Compute KPI: count page views per 1 minute sliding window
kpi_df = df_parsed \
    .withWatermark("timestamp", "2 minutes") \
    .groupBy(window(col("timestamp"), "1 minute", "30 seconds"), col("page")) \
    .agg(count("user_id").alias("page_view_count"))

# Detect anomaly: users with more than 20 clicks in 1 minute (example)
anomaly_df = df_parsed \
    .filter(col("event_type") == "click") \
    .groupBy(window(col("timestamp"), "1 minute"), col("user_id")) \
    .agg(count("event_type").alias("click_count")) \
    .filter(col("click_count") > 20)

# Write KPI results to Elasticsearch (example sink)
def write_to_elasticsearch(batch_df, batch_id):
    es = Elasticsearch(["http://localhost:9200"])
    for row in batch_df.collect():
        doc = row.asDict()
        es.index(index="kpi_results", body=doc)

# Start streaming query for KPI
def start_kpi_query():
    return kpi_df.writeStream \
        .outputMode("update") \
        .foreachBatch(write_to_elasticsearch) \
        .option("checkpointLocation", "./checkpoint_kpi") \
        .start()

# Start streaming query for anomaly detection
def start_anomaly_query():
    return anomaly_df.writeStream \
        .outputMode("update") \
        .foreachBatch(write_to_elasticsearch) \
        .option("checkpointLocation", "./checkpoint_anomaly") \
        .start()

if __name__ == "__main__":
    kpi_query = start_kpi_query()
    anomaly_query = start_anomaly_query()
    print("Streaming started. Press Ctrl+C to stop.")
    kpi_query.awaitTermination()
    anomaly_query.awaitTermination() 