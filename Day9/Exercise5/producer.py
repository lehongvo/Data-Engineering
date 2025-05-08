#!/usr/bin/env python3
import json
import random
import time
import logging
import sys
from datetime import datetime
from kafka import KafkaProducer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("producer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("sensor-producer")

# Create producer
try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Successfully connected to Kafka producer")
except Exception as e:
    logger.error(f"Cannot connect to Kafka: {e}")
    sys.exit(1)

# Function to generate valid sensor data
def generate_valid_data():
    return {
        "sensor_id": random.randint(1, 10),
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(15, 35), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "status": random.choice(["normal", "warning", "critical"])
    }

# Function to generate invalid sensor data (creating different types of errors)
def generate_invalid_data():
    # Randomly choose an error type
    error_type = random.choice([
        "missing_field",
        "invalid_type",
        "out_of_range",
        "invalid_format",
        "null_value"
    ])
    
    # Start with valid data
    data = generate_valid_data()
    
    # Create errors based on chosen error type
    if error_type == "missing_field":
        # Remove a random field
        field_to_remove = random.choice(list(data.keys()))
        del data[field_to_remove]
        data["_error_type"] = f"missing_field:{field_to_remove}"
    
    elif error_type == "invalid_type":
        # Set a field to an invalid data type
        if random.choice([True, False]):
            data["temperature"] = "not_a_number"
            data["_error_type"] = "invalid_type:temperature"
        else:
            data["humidity"] = "invalid_value"
            data["_error_type"] = "invalid_type:humidity"
    
    elif error_type == "out_of_range":
        # Set a value outside the valid range
        if random.choice([True, False]):
            data["temperature"] = random.choice([-50, 150])
            data["_error_type"] = "out_of_range:temperature"
        else:
            data["humidity"] = random.choice([-10, 150])
            data["_error_type"] = "out_of_range:humidity"
    
    elif error_type == "invalid_format":
        # Invalid timestamp format
        data["timestamp"] = "invalid-timestamp-format"
        data["_error_type"] = "invalid_format:timestamp"
    
    elif error_type == "null_value":
        # Set a field to null
        field_to_nullify = random.choice(["sensor_id", "temperature", "humidity"])
        data[field_to_nullify] = None
        data["_error_type"] = f"null_value:{field_to_nullify}"
    
    return data

# Send data continuously
try:
    counter = 0
    while True:
        # Generate and send valid or invalid data based on probability
        # 20% chance to create invalid data
        if random.random() < 0.2:
            data = generate_invalid_data()
            logger.info(f"Sending invalid data: {data}")
        else:
            data = generate_valid_data()
            logger.info(f"Sending valid data: {data}")
        
        # Send data to Kafka
        producer.send('sensor-data', value=data)
        
        # Count and send tracking status
        counter += 1
        if counter % 10 == 0:
            logger.info(f"Sent {counter} records")
        
        # Wait a random amount of time before sending the next record
        time.sleep(random.uniform(0.5, 2))

except KeyboardInterrupt:
    logger.info("Interrupted by user, stopping producer")
except Exception as e:
    logger.error(f"Error sending data: {e}")
finally:
    # Ensure all messages are sent before exiting
    producer.flush()
    logger.info("Producer stopped") 