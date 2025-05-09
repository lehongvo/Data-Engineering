#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kafka Streams implementation in Python for sales data analysis
- Calculates total revenue by product category per hour
- Used for performance comparison with Apache Flink
"""

import json
import os
import time
import argparse
import logging
from datetime import datetime, timedelta
from confluent_kafka import Producer, Consumer
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("KafkaSalesAnalysis")

# Kafka topic configuration
INPUT_TOPIC = "sales-data"
OUTPUT_TOPIC = "hourly-revenue"

def load_data_to_kafka(input_file: str, bootstrap_servers: str = "localhost:9092"):
    """Load sales data from file to Kafka topic."""
    logger.info(f"Loading data from {input_file} to Kafka topic {INPUT_TOPIC}")
    
    # Configure Kafka producer
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': 'sales-data-producer'
    }
    
    producer = Producer(producer_config)
    
    # Count for logging progress
    count = 0
    
    # Read and send each line of the input file
    with open(input_file, 'r') as f:
        for line in f:
            try:
                # Parse JSON record
                record = json.loads(line)
                
                # Use sale_id as key
                key = record["sale_id"]
                
                # Produce to Kafka topic
                producer.produce(
                    INPUT_TOPIC,
                    key=key.encode('utf-8'),
                    value=line.encode('utf-8')
                )
                
                count += 1
                if count % 10000 == 0:
                    producer.flush()
                    logger.info(f"Loaded {count} records to Kafka")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON: {e}")
            except Exception as e:
                logger.error(f"Error sending to Kafka: {e}")
    
    # Final flush to ensure all messages are sent
    producer.flush()
    logger.info(f"Loaded total of {count} records to Kafka")

def process_data(output_dir: str, bootstrap_servers: str = "localhost:9092"):
    """Process sales data with Kafka consumer/producer pattern."""
    logger.info("Starting Kafka sales data processing")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure Kafka consumer
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'sales-analysis-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    }
    
    consumer = Consumer(consumer_config)
    consumer.subscribe([INPUT_TOPIC])
    
    # Configure Kafka producer for output
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': 'sales-analysis-producer'
    }
    
    producer = Producer(producer_config)
    
    # State to hold aggregated data
    # Structure: {category}_{hour} -> total_revenue
    hourly_revenue = {}
    
    try:
        # Process messages with a timeout
        start_time = time.time()
        timeout = 300  # 5 minutes timeout
        
        while time.time() - start_time < timeout:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
            
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue
                
            try:
                # Parse the message value
                record = json.loads(msg.value().decode('utf-8'))
                
                # Extract data
                category = record["product_category"]
                timestamp_str = record["timestamp"]
                total_amount = float(record["total_amount"])
                
                # Parse timestamp and extract hour
                dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                hour_key = dt.strftime("%Y-%m-%d %H:00:00")
                hour_end = (dt.replace(minute=0, second=0) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                
                # Create a unique key for category and hour
                aggregation_key = f"{category}_{hour_key}"
                
                # Aggregate data
                if aggregation_key in hourly_revenue:
                    hourly_revenue[aggregation_key]["total_revenue"] += total_amount
                else:
                    hourly_revenue[aggregation_key] = {
                        "product_category": category,
                        "window_start": hour_key,
                        "window_end": hour_end,
                        "total_revenue": total_amount
                    }
                
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing message: {e}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
        
        # Send aggregated results to output topic and save to file
        output_file = os.path.join(output_dir, "hourly_revenue.json")
        with open(output_file, 'w') as f:
            for key, value in hourly_revenue.items():
                # Send to Kafka topic
                producer.produce(
                    OUTPUT_TOPIC,
                    key=value["product_category"].encode('utf-8'),
                    value=json.dumps(value).encode('utf-8')
                )
                
                # Write to file
                f.write(json.dumps(value) + "\n")
                
        producer.flush()
        logger.info(f"Results written to {output_file}")
        
    finally:
        consumer.close()

def main():
    parser = argparse.ArgumentParser(description='Kafka Sales Data Analysis in Python')
    parser.add_argument('--input', type=str, required=True, 
                        help='Input file path')
    parser.add_argument('--output', type=str, required=True, 
                        help='Output directory path')
    parser.add_argument('--bootstrap-servers', type=str, default='localhost:9092',
                        help='Kafka bootstrap servers')
    
    args = parser.parse_args()
    
    # Record start time for benchmarking
    start_time = time.time()
    
    # Load data to Kafka
    load_data_to_kafka(args.input, args.bootstrap_servers)
    
    # Process data
    process_data(args.output, args.bootstrap_servers)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    logger.info(f"Job executed successfully in {execution_time:.2f} seconds!")
    
    # Write performance metrics
    metrics_file = os.path.join(os.path.dirname(args.output), "kafka_metrics.json")
    metrics = {
        "framework": "Kafka (Python)",
        "execution_time_seconds": execution_time,
        "input_file": args.input,
        "output_directory": args.output
    }
    
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logger.info(f"Performance metrics saved to {metrics_file}")

if __name__ == "__main__":
    main() 