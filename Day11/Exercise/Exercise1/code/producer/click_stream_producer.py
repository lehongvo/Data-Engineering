from kafka import KafkaProducer
import json
import time
import random
import datetime
import uuid
import logging
import socket
import os

# Set up logging
LOG_DIR = "/data/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "kafka_producer.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("KafkaProducer")
logger.info(f"Logging to file: {LOG_FILE}")

def generate_clickstream_data():
    """Generate random clickstream data"""
    users = ['user1', 'user2', 'user3', 'user4', 'user5']
    pages = ['/home', '/products', '/about', '/contact', '/cart', '/checkout']
    actions = ['view', 'click', 'scroll', 'hover']
    devices = ['mobile', 'desktop', 'tablet']
    
    return {
        'event_id': str(uuid.uuid4()),
        'user_id': random.choice(users),
        'page': random.choice(pages),
        'action': random.choice(actions),
        'device': random.choice(devices),
        'timestamp': datetime.datetime.now().isoformat(),
        'session_duration': random.randint(1, 300),  # seconds
        'referrer': random.choice(['google', 'facebook', 'twitter', 'direct', None])
    }

def main():
    # Log producer start
    logger.info("Initializing Kafka producer")
    logger.info(f"Hostname: {socket.gethostname()}")
    
    try:
        # Create Kafka producer
        # Try first with localhost, then with container name if that fails
        try:
            producer = KafkaProducer(
                bootstrap_servers=['localhost:9094'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Successfully connected to Kafka broker at localhost:9094")
        except Exception as e:
            logger.warning(f"Failed to connect to localhost:9094: {e}")
            logger.info("Trying e1-kafka:9092 instead...")
            producer = KafkaProducer(
                bootstrap_servers=['e1-kafka:9092'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Successfully connected to Kafka broker at e1-kafka:9092")
    except Exception as e:
        logger.error(f"Failed to connect to Kafka broker: {e}")
        return
    
    # Send data every second
    message_count = 0
    while True:
        try:
            data = generate_clickstream_data()
            future = producer.send('clickstream', data)
            # Wait for message to be sent and log metadata
            metadata = future.get(timeout=10)
            message_count += 1
            
            if message_count % 10 == 0:
                logger.info(f"Successfully sent {message_count} messages to topic {metadata.topic}, partition {metadata.partition}")
            logger.debug(f"Sent: {data}")
            
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            time.sleep(5)

if __name__ == "__main__":
    logger.info("Starting Clickstream Producer...")
    logger.info("Waiting for Kafka to be fully up...")
    time.sleep(10)  # Wait for Kafka to be fully up
    main() 