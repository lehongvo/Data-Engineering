#!/usr/bin/env python3
import json
import logging
import sys
import time
from datetime import datetime, timedelta
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stream_processor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("stream-processor")

# Kafka configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
CONSUMER_GROUP = 'sensor-stream-processor'

# Create Kafka consumer
consumer_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': CONSUMER_GROUP,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
}

# Create Kafka producer
producer_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
}

# Initialize consumer and producer
try:
    consumer = Consumer(consumer_config)
    producer = Producer(producer_config)
    logger.info("Successfully connected to Kafka")
except KafkaException as e:
    logger.error(f"Failed to connect to Kafka: {e}")
    sys.exit(1)

# Subscribe to the topics
consumer.subscribe(['temperature-data', 'humidity-data', 'pressure-data'])

# Window size for time-windowed aggregation (in seconds)
WINDOW_SIZE = 60  # 1 minute window

# Cache for joining streams (keyed by location and timestamp window)
# We'll use a 5-second window for joining records from different topics
join_cache = {}
JOIN_WINDOW = 5  # seconds

# Storage for time-windowed aggregation
window_data = defaultdict(lambda: defaultdict(list))

def delivery_report(err, msg):
    """Callback for message delivery reports"""
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")

def detect_anomalies(message_data):
    """
    Feature 1: Detect anomalies in sensor data and send alerts
    """
    if message_data.get('is_anomaly', False):
        # This is an anomaly, send an alert
        topic = 'anomaly-alerts'
        
        # Create an alert message
        sensor_type = 'temperature' if 'temperature' in message_data else \
                     'humidity' if 'humidity' in message_data else 'pressure'
        value = message_data.get('temperature' if sensor_type == 'temperature' else 
                                'humidity' if sensor_type == 'humidity' else 'pressure')
        
        alert_message = {
            'timestamp': message_data['timestamp'],
            'location': message_data['location'],
            'sensor_id': message_data['sensor_id'],
            'sensor_type': sensor_type,
            'value': value,
            'alert_message': f"Anomaly detected: {sensor_type} reading of {value} at {message_data['location']}"
        }
        
        # Send the alert
        producer.produce(
            topic,
            json.dumps(alert_message).encode('utf-8'),
            callback=delivery_report
        )
        producer.flush()
        
        logger.info(f"Alert sent: {alert_message['alert_message']}")
        return True
    return False

def process_time_windows():
    """
    Feature 2: Calculate averages for sensor readings over time windows
    """
    current_time = datetime.now()
    results = []
    
    # Process each location and sensor type window
    for location, sensor_data in window_data.items():
        window_results = {
            'location': location,
            'timestamp': current_time.isoformat(),
            'window_size_seconds': WINDOW_SIZE
        }
        
        # Process each sensor type
        for sensor_type, readings in sensor_data.items():
            # Filter to include only readings within the window
            window_start = current_time - timedelta(seconds=WINDOW_SIZE)
            valid_readings = []
            
            for reading in readings:
                reading_time = datetime.fromisoformat(reading['timestamp'])
                if reading_time >= window_start:
                    valid_readings.append(reading)
            
            # Calculate average if there are readings
            if valid_readings:
                if sensor_type == 'temperature':
                    values = [r['temperature'] for r in valid_readings]
                    window_results['avg_temperature'] = sum(values) / len(values)
                    window_results['temperature_reading_count'] = len(values)
                
                elif sensor_type == 'humidity':
                    values = [r['humidity'] for r in valid_readings]
                    window_results['avg_humidity'] = sum(values) / len(values)
                    window_results['humidity_reading_count'] = len(values)
                
                elif sensor_type == 'pressure':
                    values = [r['pressure'] for r in valid_readings]
                    window_results['avg_pressure'] = sum(values) / len(values)
                    window_results['pressure_reading_count'] = len(values)
        
        # Only include windows with data
        if len(window_results) > 3:  # More than just location, timestamp, and window_size
            results.append(window_results)
            
            # Send window aggregate to Kafka
            producer.produce(
                'window-aggregates',
                json.dumps(window_results).encode('utf-8'),
                callback=delivery_report
            )
    
    # Clean up old data
    cleanup_window_data(current_time - timedelta(seconds=WINDOW_SIZE))
    
    return results

def cleanup_window_data(cutoff_time):
    """Remove readings older than the cutoff time from window data"""
    for location, sensor_data in window_data.items():
        for sensor_type, readings in sensor_data.items():
            window_data[location][sensor_type] = [
                reading for reading in readings 
                if datetime.fromisoformat(reading['timestamp']) >= cutoff_time
            ]

def process_joins(message_data, topic):
    """
    Feature 3: Join data from multiple sensor streams for the same location
    """
    location = message_data['location']
    timestamp = datetime.fromisoformat(message_data['timestamp'])
    
    # Create a key based on location and rounded timestamp (for the join window)
    # This allows us to join messages that are close in time but not exactly the same
    timestamp_key = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    join_key = f"{location}_{timestamp_key}"
    
    # Initialize join cache entry if needed
    if join_key not in join_cache:
        join_cache[join_key] = {
            'temperature': None,
            'humidity': None,
            'pressure': None,
            'created_at': timestamp,
        }
    
    # Determine message type and store in the appropriate field
    if topic == 'temperature-data' and 'temperature' in message_data:
        join_cache[join_key]['temperature'] = message_data
    elif topic == 'humidity-data' and 'humidity' in message_data:
        join_cache[join_key]['humidity'] = message_data
    elif topic == 'pressure-data' and 'pressure' in message_data:
        join_cache[join_key]['pressure'] = message_data
    
    # Check if we have data from all three sources
    cache_entry = join_cache[join_key]
    if cache_entry['temperature'] and cache_entry['humidity'] and cache_entry['pressure']:
        # We have all three! Create a joined record
        joined_data = {
            'timestamp': timestamp.isoformat(),
            'location': location,
            'temperature': cache_entry['temperature']['temperature'],
            'humidity': cache_entry['humidity']['humidity'],
            'pressure': cache_entry['pressure']['pressure'],
            'joined_from': [
                cache_entry['temperature']['sensor_id'],
                cache_entry['humidity']['sensor_id'],
                cache_entry['pressure']['sensor_id']
            ]
        }
        
        # Send the joined data to Kafka
        producer.produce(
            'joined-sensor-data',
            json.dumps(joined_data).encode('utf-8'),
            callback=delivery_report
        )
        producer.flush()
        
        logger.info(f"Joined data for {location} at {timestamp_key}")
        
        # Remove this entry from the cache since it's been processed
        del join_cache[join_key]
        return joined_data
    
    return None

def cleanup_join_cache():
    """Clean up old entries from the join cache"""
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(seconds=JOIN_WINDOW)
    
    keys_to_remove = []
    for key, entry in join_cache.items():
        if entry['created_at'] < cutoff_time:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del join_cache[key]
    
    if keys_to_remove:
        logger.debug(f"Cleaned up {len(keys_to_remove)} old join cache entries")

# Main processing loop
last_window_process_time = datetime.now()

try:
    logger.info("Starting Kafka Streams processor...")
    
    while True:
        # Poll for new messages
        msg = consumer.poll(1.0)
        
        if msg is None:
            # No message received, continue
            pass
        elif msg.error():
            # Error in message, log and continue
            logger.error(f"Consumer error: {msg.error()}")
        else:
            # Process message
            try:
                # Decode the message
                message_value = msg.value().decode('utf-8')
                message_data = json.loads(message_value)
                topic = msg.topic()
                
                # Store data for time-windowed processing
                if 'location' in message_data:
                    location = message_data['location']
                    
                    if topic == 'temperature-data' and 'temperature' in message_data:
                        window_data[location]['temperature'].append(message_data)
                    elif topic == 'humidity-data' and 'humidity' in message_data:
                        window_data[location]['humidity'].append(message_data)
                    elif topic == 'pressure-data' and 'pressure' in message_data:
                        window_data[location]['pressure'].append(message_data)
                
                # Feature 1: Detect anomalies
                detect_anomalies(message_data)
                
                # Feature 3: Join multiple streams
                process_joins(message_data, topic)
                
                # Commit the message
                consumer.commit(msg)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
        
        # Feature 2: Process time windows periodically (every 10 seconds)
        current_time = datetime.now()
        if (current_time - last_window_process_time).total_seconds() >= 10:
            process_time_windows()
            last_window_process_time = current_time
        
        # Clean up the join cache periodically
        cleanup_join_cache()
        
        # Give the CPU a break
        time.sleep(0.01)

except KeyboardInterrupt:
    logger.info("Interrupted by user, shutting down...")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
finally:
    # Close the consumer
    consumer.close()
    logger.info("Stream processor stopped.") 