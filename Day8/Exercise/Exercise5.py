# Exercise 5: Real-Time Analytics with Kafka and Spark Streaming
# Requirements: pyspark, kafka-python, elasticsearch
# Install: pip install pyspark kafka-python elasticsearch

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from elasticsearch import Elasticsearch
import json
import socket
import time
import sys

# Define schema for incoming events (example: page view event)
event_schema = StructType([
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("page", StringType()),
    StructField("product_id", StringType()),
])

# Function to check if Kafka is available
def is_kafka_available(host="localhost", port=9092):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingExercise5") \
    .getOrCreate()

# Kafka configuration
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "page_views"

# Check if Kafka is available
kafka_available = is_kafka_available()
print(f"Kafka availability check: {'Available' if kafka_available else 'Not Available'}")

if kafka_available:
    # Real Kafka mode: Read stream from Kafka
    df_raw = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "latest") \
        .load()

    # Parse value as JSON
    df_parsed = df_raw.select(from_json(col("value").cast("string"), event_schema).alias("data")).select("data.*")
else:
    # Simulation mode: Generate sample data
    print("Running in simulation mode with generated data")
    # Create a simulated static dataframe with some sample data
    sample_data = [
        ("user1", "view", "2023-05-06T08:00:00.000Z", "home", "product1"),
        ("user2", "click", "2023-05-06T08:01:00.000Z", "product", "product2"),
        ("user3", "view", "2023-05-06T08:02:00.000Z", "cart", "product3")
    ]
    
    static_df = spark.createDataFrame(sample_data, ["user_id", "event_type", "timestamp_str", "page", "product_id"])
    static_df = static_df.withColumn("timestamp", current_timestamp())
    
    # Create streaming dataframe from static data - for demo purposes
    df_parsed = spark.readStream.format("rate").option("rowsPerSecond", 1).load() \
        .join(static_df.select("user_id", "event_type", "page", "product_id"), how="cross") \
        .withColumn("timestamp", current_timestamp())

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

# Write KPI results to console for demo (since Elasticsearch might not be available)
def start_kpi_query():
    return kpi_df.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", "false") \
        .start()

# Write anomaly results to console for demo
def start_anomaly_query():
    return anomaly_df.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", "false") \
        .start()

if __name__ == "__main__":
    try:
        kpi_query = start_kpi_query()
        anomaly_query = start_anomaly_query()
        print("Streaming started. Press Ctrl+C to stop.")
        
        # Create a simple terminal progress bar
        i = 0
        while True:
            time.sleep(5)
            i += 1
            sys.stdout.write(f"\rProcessing events... {i*5}s elapsed")
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print("\nStopping streams...")
    finally:
        spark.stop() 