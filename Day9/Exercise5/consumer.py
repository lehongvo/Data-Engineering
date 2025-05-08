#!/usr/bin/env python3
import json
import logging
import sys
import time
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("consumer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("sensor-consumer")

# Create consumer connected to Kafka
try:
    consumer = KafkaConsumer(
        'sensor-data',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='sensor-processing-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Successfully connected to Kafka consumer")

    # Create producer for DLQ
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Successfully connected to Kafka DLQ producer")
except Exception as e:
    logger.error(f"Cannot connect to Kafka: {e}")
    sys.exit(1)

# Define validation functions
def is_valid_timestamp(timestamp_str):
    try:
        # Check ISO datetime format
        datetime.fromisoformat(timestamp_str)
        return True
    except (ValueError, TypeError):
        return False

def is_valid_temperature(temp):
    if not isinstance(temp, (int, float)):
        return False
    return 0 <= temp <= 100  # Valid temperature range: 0 to 100°C

def is_valid_humidity(humidity):
    if not isinstance(humidity, (int, float)):
        return False
    return 0 <= humidity <= 100  # Valid humidity range: 0 to 100%

def is_valid_sensor_id(sensor_id):
    if not isinstance(sensor_id, int):
        return False
    return 1 <= sensor_id <= 10  # Valid sensor ID range: 1-10

def is_valid_status(status):
    return status in ["normal", "warning", "critical"]

# Function to validate the entire record
def validate_record(record):
    validation_errors = []
    
    # Check required fields
    required_fields = ["sensor_id", "timestamp", "temperature", "humidity", "status"]
    for field in required_fields:
        if field not in record:
            validation_errors.append(f"Missing required field: {field}")
    
    # If fields are missing, no need to check further
    if validation_errors:
        return False, validation_errors
    
    # Check data types and values
    if not is_valid_sensor_id(record["sensor_id"]):
        validation_errors.append("Invalid sensor ID")
    
    if not is_valid_timestamp(record["timestamp"]):
        validation_errors.append("Invalid timestamp")
    
    if not is_valid_temperature(record["temperature"]):
        validation_errors.append("Invalid temperature")
    
    if not is_valid_humidity(record["humidity"]):
        validation_errors.append("Invalid humidity")
    
    if not is_valid_status(record["status"]):
        validation_errors.append("Invalid status")
    
    return len(validation_errors) == 0, validation_errors

# Function to process a record
def process_record(record):
    # Simulate data processing (would do more in real-world scenario)
    logger.info(f"Processing record from sensor {record['sensor_id']}: " +
               f"temperature={record.get('temperature')}, humidity={record.get('humidity')}, " +
               f"status={record.get('status')}")
    
    # Could perform calculations or store data here
    return True

# Function to send error record to DLQ
def send_to_dlq(record, validation_errors):
    # Add error information to the record
    error_record = record.copy()
    error_record["_validation_errors"] = validation_errors
    error_record["_error_timestamp"] = datetime.now().isoformat()
    
    # Send to DLQ topic
    producer.send('dead-letter-queue', value=error_record)
    logger.warning(f"Sent error record to DLQ: {error_record}")

# Process records from Kafka
try:
    valid_count = 0
    error_count = 0
    
    logger.info("Starting to listen for records from 'sensor-data' topic...")
    for message in consumer:
        try:
            record = message.value
            
            # Validate the record
            is_valid, errors = validate_record(record)
            
            if is_valid:
                # Process valid record
                process_record(record)
                valid_count += 1
                
                if valid_count % 10 == 0:
                    logger.info(f"Processed {valid_count} valid records, {error_count} error records")
            else:
                # Send invalid record to DLQ
                send_to_dlq(record, errors)
                error_count += 1
        
        except Exception as e:
            logger.error(f"Error processing record: {e}")
            # Send record with error to DLQ
            send_to_dlq(record, [f"Exception: {str(e)}"])
            error_count += 1

except KeyboardInterrupt:
    logger.info("Interrupted by user, stopping consumer")
except Exception as e:
    logger.error(f"Unidentified error: {e}")
finally:
    try:
        consumer.close()
        producer.close()
    except:
        pass
    logger.info(f"Consumer stopped. Total: {valid_count} valid records, {error_count} error records") 