#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import random
import logging
import os
from datetime import datetime
from kafka import KafkaProducer
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
        logging.FileHandler("../logs/kafka_producer.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("stock-market-producer")

# List of sample stocks
STOCKS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "META", 
    "TSLA", "NVDA", "PYPL", "ADBE", "NFLX"
]

class StockMarketProducer:
    def __init__(self, bootstrap_servers='localhost:9092', topic_name='stock-market-data'):
        """Initialize Stock Market producer with Kafka connection."""
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        
        # Initialize Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None
        )
        
        logger.info(f"Producer initialized with bootstrap servers: {bootstrap_servers}")
        logger.info(f"Producing to topic: {topic_name}")

    def generate_stock_data(self):
        """Generate random stock market data."""
        stock = random.choice(STOCKS)
        timestamp = datetime.now().isoformat()
        price = round(random.uniform(50, 500), 2)
        volume = random.randint(1000, 10000)
        
        return {
            "symbol": stock,
            "timestamp": timestamp,
            "price": price,
            "volume": volume,
            "change_percent": round(random.uniform(-5, 5), 2)
        }

    def send_to_kafka(self, data):
        """Send stock data to Kafka topic."""
        future = self.producer.send(
            self.topic_name, 
            key=data["symbol"], 
            value=data
        )
        try:
            record_metadata = future.get(timeout=10)
            logger.info(f"Sent: {data['symbol']} - Price: {data['price']} - Volume: {data['volume']}")
            logger.debug(f"Metadata: {record_metadata}")
            return True
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {e}")
            return False

    def start_streaming(self, interval=1, count=None):
        """Start streaming stock market data to Kafka."""
        logger.info("Starting Stock Market data streaming...")
        
        produced_count = 0
        
        try:
            while count is None or produced_count < count:
                data = self.generate_stock_data()
                success = self.send_to_kafka(data)
                
                if success:
                    produced_count += 1
                
                # Sleep before next message
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, stopping...")
        except Exception as e:
            logger.error(f"Error in streaming loop: {e}")
        finally:
            self.close()
            logger.info(f"Producer stopped. Total messages produced: {produced_count}")

    def close(self):
        """Close the producer."""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")

if __name__ == "__main__":
    # Get parameters from environment or use defaults
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    topic_name = os.getenv('KAFKA_TOPIC', 'stock-market-data')
    interval = float(os.getenv('PRODUCER_INTERVAL', '1'))
    
    try:
        producer = StockMarketProducer(bootstrap_servers, topic_name)
        producer.start_streaming(interval=interval)
    except Exception as e:
        logger.error(f"Failed to start producer: {e}") 