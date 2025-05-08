#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
import logging
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count, avg, max, explode, split, to_timestamp, sum, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType, BooleanType
import findspark
from dotenv import load_dotenv
from utils import setup_logging

# Setup logging
logger = setup_logging('spark-streaming')

# Ensure environment variables are loaded
load_dotenv()

# Initialize findspark to locate Spark installation
findspark.init()

# Define schema for Ethereum transaction data
transaction_schema = StructType([
    StructField("hash", StringType(), True),
    StructField("block_number", IntegerType(), True),
    StructField("block_hash", StringType(), True),
    StructField("from", StringType(), True),
    StructField("to", StringType(), True),
    StructField("value", FloatType(), True),
    StructField("value_wei", StringType(), True),
    StructField("gas", IntegerType(), True),
    StructField("gas_price", FloatType(), True),
    StructField("nonce", IntegerType(), True),
    StructField("input_data", StringType(), True),
    StructField("transaction_index", IntegerType(), True),
    StructField("is_contract_creation", BooleanType(), True),
    StructField("is_contract_call", BooleanType(), True)
])

# Define schema for Ethereum block data
block_schema = StructType([
    StructField("number", IntegerType(), True),
    StructField("hash", StringType(), True),
    StructField("parent_hash", StringType(), True),
    StructField("timestamp", IntegerType(), True),
    StructField("datetime", StringType(), True),
    StructField("gas_used", IntegerType(), True),
    StructField("gas_limit", IntegerType(), True),
    StructField("transaction_count", IntegerType(), True),
    StructField("miner", StringType(), True),
    StructField("difficulty", StringType(), True),
    StructField("total_difficulty", StringType(), True),
    StructField("size", IntegerType(), True),
    StructField("nonce", StringType(), True),
    StructField("base_fee_per_gas", IntegerType(), True)
])

class EthereumSparkStreaming:
    def __init__(self):
        """Initialize Spark Streaming for Ethereum data processing."""
        logger.info("Initializing Spark Streaming application")
        
        # Get Kafka bootstrap servers from environment
        self.kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        
        # Create Spark session
        self.spark = SparkSession.builder \
            .appName("EthereumDataProcessing") \
            .config("spark.sql.streaming.checkpointLocation", "checkpoint") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
            .getOrCreate()
        
        # Set log level
        self.spark.sparkContext.setLogLevel("ERROR")
        
        logger.info(f"Spark session created with application ID: {self.spark.sparkContext.applicationId}")
        
    def start_streaming(self):
        """Start processing streams from Kafka."""
        try:
            # Process transactions stream
            self.process_transactions_stream()
            
            # Process blocks stream
            self.process_blocks_stream()
            
            # Keep the application running
            self.spark.streams.awaitAnyTermination()
            
        except Exception as e:
            logger.error(f"Error in Spark Streaming: {e}")
            self.spark.stop()
    
    def process_transactions_stream(self):
        """Process Ethereum transactions from Kafka."""
        logger.info("Starting to process transactions stream")
        
        # Read transaction stream from Kafka
        transactions_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", "ethereum-transactions") \
            .option("startingOffsets", "latest") \
            .load()
        
        # Parse JSON data and add processing timestamp
        parsed_transactions = transactions_df \
            .selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), transaction_schema).alias("transaction")) \
            .select("transaction.*") \
            .withColumn("event_time", current_timestamp())  # Add current timestamp for windowing
        
        # 1. High-value transactions analysis
        high_value_transactions = parsed_transactions \
            .filter(col("value") > 1.0)  # Transactions over 1 ETH
            
        # Write high-value transactions to console for demo
        high_value_query = high_value_transactions \
            .writeStream \
            .outputMode("append") \
            .format("console") \
            .option("truncate", False) \
            .option("numRows", 10) \
            .start()
        
        # 2. Transaction volume by address
        # Group by sender address and count transactions in 5-minute windows
        address_volume = parsed_transactions \
            .withWatermark("event_time", "10 minutes") \
            .groupBy(
                window(col("event_time"), "5 minutes"),
                col("from")
            ) \
            .agg(
                count("*").alias("transaction_count"),
                avg("gas_price").alias("avg_gas_price"),
                sum("value").alias("total_eth_sent")
            )
        
        # Write address volume to file sink
        address_volume_query = address_volume \
            .writeStream \
            .outputMode("append") \
            .format("csv") \
            .option("path", "output/address_volume") \
            .option("checkpointLocation", "checkpoint/address_volume") \
            .start()
        
        # 3. Contract interaction analysis
        contract_interactions = parsed_transactions \
            .filter(col("is_contract_call") == True) \
            .withWatermark("event_time", "1 hour") \
            .groupBy(
                window(col("event_time"), "1 hour"),
                col("to")  # Contract address
            ) \
            .count()
        
        # Write contract interactions to file
        contract_query = contract_interactions \
            .writeStream \
            .outputMode("complete") \
            .format("csv") \
            .option("path", "output/contract_interactions") \
            .option("checkpointLocation", "checkpoint/contract_interactions") \
            .start()
        
        logger.info("Transaction stream processing started")
    
    def process_blocks_stream(self):
        """Process Ethereum blocks from Kafka."""
        logger.info("Starting to process blocks stream")
        
        # Read blocks stream from Kafka
        blocks_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", "ethereum-blocks") \
            .option("startingOffsets", "latest") \
            .load()
        
        # Parse JSON data
        parsed_blocks = blocks_df \
            .selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), block_schema).alias("block")) \
            .select("block.*")
        
        # 1. Block time analysis - how long between blocks
        block_times = parsed_blocks \
            .withColumn("datetime", to_timestamp(col("datetime"))) \
            .withWatermark("datetime", "10 minutes") \
            .groupBy(window(col("datetime"), "10 minutes")) \
            .agg(
                count("*").alias("block_count"),
                avg("gas_used").alias("avg_gas_used"),
                max("transaction_count").alias("max_transactions")
            )
        
        # Write block time analysis to console
        block_time_query = block_times \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", False) \
            .start()
        
        # 2. Gas usage trends
        gas_trends = parsed_blocks \
            .withColumn("datetime", to_timestamp(col("datetime"))) \
            .withWatermark("datetime", "10 minutes") \
            .groupBy(window(col("datetime"), "1 hour")) \
            .agg(
                avg("gas_used").alias("avg_gas_used"),
                avg(col("gas_used") / col("gas_limit")).alias("gas_utilization_ratio")
            )
        
        # Write gas trends to file
        gas_query = gas_trends \
            .writeStream \
            .outputMode("append") \
            .format("csv") \
            .option("path", "output/gas_trends") \
            .option("checkpointLocation", "checkpoint/gas_trends") \
            .start()
        
        logger.info("Block stream processing started")

if __name__ == "__main__":
    try:
        # Create and start the Spark Streaming application
        spark_app = EthereumSparkStreaming()
        spark_app.start_streaming()
    except KeyboardInterrupt:
        logger.info("Stopping Spark Streaming application...")
    except Exception as e:
        logger.error(f"Fatal error: {e}") 