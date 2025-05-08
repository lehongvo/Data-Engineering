#!/usr/bin/env python3
import json
import logging
import sys
import time
from datetime import datetime
from collections import defaultdict, Counter
from kafka import KafkaConsumer, KafkaProducer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("dlq_consumer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("dlq-consumer")

# Create consumer connected to DLQ
try:
    consumer = KafkaConsumer(
        'dead-letter-queue',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='dlq-processing-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Successfully connected to Kafka DLQ consumer")

    # Create producer to send error analytics
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Successfully connected to Kafka producer for error analytics")
except Exception as e:
    logger.error(f"Cannot connect to Kafka: {e}")
    sys.exit(1)

# Initialize counters for tracking and analyzing errors
error_counts = Counter()
error_by_sensor = defaultdict(Counter)
validation_error_types = Counter()
last_analytics_time = time.time()
ANALYTICS_INTERVAL = 30  # Send analytics report every 30 seconds

def categorize_error(error_record):
    """Categorize errors from error records"""
    # Get error information from record
    validation_errors = error_record.get("_validation_errors", [])
    error_type = error_record.get("_error_type", "unknown")
    
    # Categorize error
    if "_error_type" in error_record:
        return error_record["_error_type"]
    elif validation_errors:
        # Use first error as the main error type
        return validation_errors[0]
    else:
        return "unknown_error"

def process_error_record(error_record):
    """Process and log error records from DLQ"""
    sensor_id = error_record.get("sensor_id", "unknown")
    error_category = categorize_error(error_record)
    validation_errors = error_record.get("_validation_errors", [])
    
    # Log detailed errors
    logger.warning(f"Error record from sensor {sensor_id}: {error_category}")
    for error in validation_errors:
        logger.warning(f" - {error}")
    
    # Update statistics
    error_counts[error_category] += 1
    error_by_sensor[sensor_id][error_category] += 1
    for error in validation_errors:
        validation_error_types[error] += 1
    
    return error_category

def send_error_analytics():
    """Send error analytics data to error-analytics topic"""
    analytics = {
        "timestamp": datetime.now().isoformat(),
        "total_errors": sum(error_counts.values()),
        "error_counts_by_type": dict(error_counts),
        "error_counts_by_sensor": {sensor: dict(counts) for sensor, counts in error_by_sensor.items()},
        "validation_error_types": dict(validation_error_types)
    }
    
    producer.send('error-analytics', value=analytics)
    logger.info(f"Sent error analytics: {len(error_counts)} error types, {sum(error_counts.values())} total errors")

# Process error records from DLQ
try:
    error_record_count = 0
    
    logger.info("Starting to listen for error records from 'dead-letter-queue'...")
    for message in consumer:
        try:
            error_record = message.value
            error_category = process_error_record(error_record)
            error_record_count += 1
            
            # Send error analytics periodically
            current_time = time.time()
            if current_time - last_analytics_time > ANALYTICS_INTERVAL:
                send_error_analytics()
                last_analytics_time = current_time
            
        except Exception as e:
            logger.error(f"Error processing DLQ record: {e}")

except KeyboardInterrupt:
    logger.info("Interrupted by user, stopping DLQ consumer")
except Exception as e:
    logger.error(f"Unidentified error: {e}")
finally:
    # Send final error analytics before exiting
    if error_counts:
        send_error_analytics()
    
    try:
        consumer.close()
        producer.close()
    except:
        pass
    
    logger.info(f"DLQ Consumer stopped. Processed {error_record_count} error records") 