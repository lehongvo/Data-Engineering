#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import logging
import csv
import time
from datetime import datetime
from kafka import KafkaConsumer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create logs directory if it doesn't exist
os.makedirs("../logs", exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../logs/kafka_consumer.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("stock-market-consumer")

class StockMarketConsumer:
    def __init__(self, bootstrap_servers='localhost:9092', topic_name='stock-market-data', 
                 group_id='stock-market-group', output_dir='../data'):
        """Initialize Stock Market consumer with Kafka connection."""
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.group_id = group_id
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            self.topic_name,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda m: m.decode('utf-8') if m else None
        )
        
        logger.info(f"Consumer initialized with bootstrap servers: {bootstrap_servers}")
        logger.info(f"Consuming from topic: {topic_name}")
        logger.info(f"Consumer group: {group_id}")
        logger.info(f"Output directory: {output_dir}")
        
        # Initialize CSV file
        self.csv_file = os.path.join(self.output_dir, f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        self.initialize_csv()

    def initialize_csv(self):
        """Initialize CSV file with headers."""
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['symbol', 'timestamp', 'price', 'volume', 'change_percent'])
            
        logger.info(f"CSV file initialized: {self.csv_file}")

    def append_to_csv(self, data):
        """Append data to CSV file."""
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['symbol'],
                data['timestamp'],
                data['price'],
                data['volume'],
                data['change_percent']
            ])

    def start_consuming(self, limit=None):
        """Start consuming messages from Kafka topic."""
        logger.info("Starting to consume stock market data...")
        
        count = 0
        
        try:
            for message in self.consumer:
                # Process message
                data = message.value
                logger.info(f"Received: {data['symbol']} - Price: {data['price']} - Volume: {data['volume']}")
                
                # Save to CSV
                self.append_to_csv(data)
                
                count += 1
                
                # Check if limit reached
                if limit is not None and count >= limit:
                    logger.info(f"Reached message limit: {limit}")
                    break
                    
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, stopping...")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
        finally:
            self.close()
            logger.info(f"Consumer stopped. Total messages consumed: {count}")
            logger.info(f"Data saved to {self.csv_file}")

    def close(self):
        """Close the consumer."""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")

if __name__ == "__main__":
    # Get parameters from environment or use defaults
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    topic_name = os.getenv('KAFKA_TOPIC', 'stock-market-data')
    group_id = os.getenv('KAFKA_CONSUMER_GROUP', 'stock-market-group')
    output_dir = os.getenv('OUTPUT_DIR', '../data')
    
    try:
        consumer = StockMarketConsumer(
            bootstrap_servers=bootstrap_servers,
            topic_name=topic_name,
            group_id=group_id,
            output_dir=output_dir
        )
        consumer.start_consuming()
    except Exception as e:
        logger.error(f"Failed to start consumer: {e}") 