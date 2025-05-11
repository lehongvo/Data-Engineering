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
LOG_DIR = "./data/logs"
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
        'event_ts': datetime.datetime.now().isoformat(timespec='milliseconds'),
        'session_duration': random.randint(1, 300),  # seconds
        'referrer': random.choice(['google', 'facebook', 'twitter', 'direct', None])
    }

def main():
    # Log producer start
    logger.info("Initializing Kafka producer")
    logger.info(f"Hostname: {socket.gethostname()}")
    
    # Define producer at a higher scope so it's accessible in the while loop
    producer = None
    connection_attempts = 0
    max_connection_attempts = 10
    
    # Send data every second
    message_count = 0
    
    while True:
        try:
            # If producer is None, try to connect
            if producer is None:
                connection_attempts += 1
                
                try:
                    # Try localhost first
                    logger.info("Trying to connect to Kafka broker at localhost:9094")
                    producer = KafkaProducer(
                        bootstrap_servers=['localhost:9094'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                        acks='all',  # Wait for all replicas to acknowledge the message
                        retries=3,   # Retry sending if fails
                        request_timeout_ms=10000  # 10 seconds timeout for requests
                    )
                    logger.info("Successfully connected to Kafka broker at localhost:9094")
                    # Reset connection attempts counter
                    connection_attempts = 0
                except Exception as e:
                    logger.warning(f"Failed to connect to localhost:9094: {e}")
                    logger.info("Trying e1-kafka:9092 instead...")
                    try:
                        producer = KafkaProducer(
                            bootstrap_servers=['e1-kafka:9092'],
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                            acks='all',  # Wait for all replicas to acknowledge the message
                            retries=3,   # Retry sending if fails
                            request_timeout_ms=10000  # 10 seconds timeout for requests
                        )
                        logger.info("Successfully connected to Kafka broker at e1-kafka:9092")
                        # Reset connection attempts counter
                        connection_attempts = 0
                    except Exception as e2:
                        logger.error(f"Failed to connect to e1-kafka:9092: {e2}")
                        if connection_attempts >= max_connection_attempts:
                            logger.error(f"Failed to connect to any Kafka broker after {connection_attempts} attempts")
                            # Wait longer between retries after many failures
                            time.sleep(10)
                        continue
            
            # Generate and send data
            data = generate_clickstream_data()
            future = producer.send('clickstream', data)
            # Wait for message to be sent and log metadata
            metadata = future.get(timeout=10)
            message_count += 1
            
            if message_count % 10 == 0:
                logger.info(f"Successfully sent {message_count} messages to topic {metadata.topic}, partition {metadata.partition}")
            logger.debug(f"Sent: {data}")
            
            # Wait 1 second between messages
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            # Reset producer on error so connection will be retried
            if producer is not None:
                try:
                    producer.close()  # Close the producer properly
                except:
                    pass
                producer = None
            # Wait before retrying
            time.sleep(5)

if __name__ == "__main__":
    logger.info("Starting Clickstream Producer...")
    logger.info("Waiting for Kafka to be fully up...")
    time.sleep(10)  # Wait for Kafka to be fully up
    main() 