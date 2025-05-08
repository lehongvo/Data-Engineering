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
        logging.FileHandler("sensor_producer.log"),
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

# Define sensor locations
LOCATIONS = ["living_room", "kitchen", "bedroom", "bathroom", "outdoor"]

# Define normal ranges for readings
TEMP_RANGE = {
    "living_room": (18, 25),
    "kitchen": (20, 28),
    "bedroom": (16, 23),
    "bathroom": (20, 30),
    "outdoor": (5, 35)
}

HUMIDITY_RANGE = {
    "living_room": (30, 50),
    "kitchen": (40, 60),
    "bedroom": (30, 45),
    "bathroom": (50, 70),
    "outdoor": (20, 80)
}

PRESSURE_RANGE = {
    "living_room": (1010, 1020),
    "kitchen": (1010, 1020),
    "bedroom": (1010, 1020),
    "bathroom": (1010, 1020),
    "outdoor": (990, 1030)
}

def generate_sensor_data(sensor_type, location, include_anomaly=False):
    """Generate sensor data with the option to include anomalies"""
    timestamp = datetime.now().isoformat()
    sensor_id = f"{location}-{sensor_type}-sensor"
    
    # Base record structure
    record = {
        "sensor_id": sensor_id,
        "location": location,
        "timestamp": timestamp
    }
    
    # Determine if we should generate an anomaly (10% chance if include_anomaly is True)
    generate_anomaly = include_anomaly and random.random() < 0.1
    
    # Add the specific reading based on sensor type
    if sensor_type == "temperature":
        if generate_anomaly:
            # Generate anomaly: extremely high or low temperature
            record["temperature"] = random.choice([
                round(random.uniform(-10, 0), 1),  # Very cold
                round(random.uniform(40, 50), 1)   # Very hot
            ])
            record["is_anomaly"] = True
            logger.warning(f"Generated temperature anomaly: {record['temperature']}°C at {location}")
        else:
            min_temp, max_temp = TEMP_RANGE[location]
            record["temperature"] = round(random.uniform(min_temp, max_temp), 1)
            record["is_anomaly"] = False
    
    elif sensor_type == "humidity":
        if generate_anomaly:
            # Generate anomaly: extremely high or low humidity
            record["humidity"] = random.choice([
                round(random.uniform(0, 15), 1),    # Very dry
                round(random.uniform(85, 100), 1)   # Very humid
            ])
            record["is_anomaly"] = True
            logger.warning(f"Generated humidity anomaly: {record['humidity']}% at {location}")
        else:
            min_hum, max_hum = HUMIDITY_RANGE[location]
            record["humidity"] = round(random.uniform(min_hum, max_hum), 1)
            record["is_anomaly"] = False
    
    elif sensor_type == "pressure":
        if generate_anomaly:
            # Generate anomaly: extremely high or low pressure
            record["pressure"] = random.choice([
                round(random.uniform(950, 980), 1),    # Very low pressure
                round(random.uniform(1040, 1060), 1)   # Very high pressure
            ])
            record["is_anomaly"] = True
            logger.warning(f"Generated pressure anomaly: {record['pressure']} hPa at {location}")
        else:
            min_press, max_press = PRESSURE_RANGE[location]
            record["pressure"] = round(random.uniform(min_press, max_press), 1)
            record["is_anomaly"] = False
    
    return record

def send_sensor_data(topic, data):
    """Send sensor data to the specified Kafka topic"""
    future = producer.send(topic, value=data)
    try:
        record_metadata = future.get(timeout=10)
        logger.debug(f"Sent to {record_metadata.topic}[{record_metadata.partition}] @ {record_metadata.offset}")
    except Exception as e:
        logger.error(f"Error sending to Kafka: {e}")

# Main execution
try:
    counter = 0
    while True:
        # For each location, send temperature, humidity, and pressure data
        for location in LOCATIONS:
            # 15% chance to include an anomaly
            include_anomaly = random.random() < 0.15
            
            # Generate and send temperature data
            temp_data = generate_sensor_data("temperature", location, include_anomaly)
            send_sensor_data("temperature-data", temp_data)
            
            # Generate and send humidity data
            humidity_data = generate_sensor_data("humidity", location, include_anomaly)
            send_sensor_data("humidity-data", humidity_data)
            
            # Generate and send pressure data
            pressure_data = generate_sensor_data("pressure", location, include_anomaly)
            send_sensor_data("pressure-data", pressure_data)
        
        counter += 1
        if counter % 10 == 0:
            logger.info(f"Sent {counter * 3 * len(LOCATIONS)} sensor readings")
        
        # Wait a bit between rounds of data generation
        time.sleep(random.uniform(0.5, 2))

except KeyboardInterrupt:
    logger.info("Producer interrupted. Shutting down...")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
finally:
    producer.flush()
    logger.info("Producer stopped.") 