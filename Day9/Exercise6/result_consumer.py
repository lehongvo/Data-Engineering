#!/usr/bin/env python3
import json
import logging
import sys
import time
from datetime import datetime
from prettytable import PrettyTable
from confluent_kafka import Consumer, KafkaException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("result_consumer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("result-consumer")

# Kafka configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
CONSUMER_GROUP = 'result-display-group'

# Create Kafka consumer
consumer_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': CONSUMER_GROUP,
    'auto.offset.reset': 'earliest',
}

# Initialize consumer
try:
    consumer = Consumer(consumer_config)
    logger.info("Successfully connected to Kafka")
except KafkaException as e:
    logger.error(f"Failed to connect to Kafka: {e}")
    sys.exit(1)

# Subscribe to the result topics
consumer.subscribe(['anomaly-alerts', 'window-aggregates', 'joined-sensor-data'])

# Counters for statistics
stats = {
    'anomalies': 0,
    'windows': 0,
    'joins': 0
}

# Last display time for each type of report
last_display = {
    'anomalies': datetime.min,
    'windows': datetime.min,
    'joins': datetime.min
}

# Storage for recent data
recent_anomalies = []
recent_windows = {}  # Keyed by location
recent_joins = []

def display_anomaly_alerts():
    """Display a table of recent anomaly alerts"""
    if not recent_anomalies:
        logger.info("No recent anomaly alerts to display")
        return
    
    logger.info(f"=== ANOMALY ALERTS (Last {len(recent_anomalies)}) ===")
    
    table = PrettyTable()
    table.field_names = ["Time", "Location", "Sensor Type", "Value", "Alert Message"]
    
    for alert in recent_anomalies:
        timestamp = datetime.fromisoformat(alert['timestamp']).strftime("%H:%M:%S")
        table.add_row([
            timestamp,
            alert['location'],
            alert['sensor_type'],
            alert['value'],
            alert['alert_message']
        ])
    
    print("\n" + str(table))
    logger.info("Total anomalies detected: " + str(stats['anomalies']))

def display_window_aggregates():
    """Display a table of recent window aggregates by location"""
    if not recent_windows:
        logger.info("No recent window aggregates to display")
        return
    
    logger.info(f"=== WINDOW AGGREGATES (Last {len(recent_windows)}) ===")
    
    table = PrettyTable()
    table.field_names = [
        "Location", 
        "Avg Temp (°C)", 
        "Readings", 
        "Avg Humidity (%)", 
        "Readings",
        "Avg Pressure (hPa)",
        "Readings",
        "Window Size (s)"
    ]
    
    for location, window in recent_windows.items():
        table.add_row([
            location,
            f"{window.get('avg_temperature', 'N/A'):.1f}" if 'avg_temperature' in window else "N/A",
            window.get('temperature_reading_count', 0),
            f"{window.get('avg_humidity', 'N/A'):.1f}" if 'avg_humidity' in window else "N/A",
            window.get('humidity_reading_count', 0),
            f"{window.get('avg_pressure', 'N/A'):.1f}" if 'avg_pressure' in window else "N/A",
            window.get('pressure_reading_count', 0),
            window.get('window_size_seconds', 'N/A')
        ])
    
    print("\n" + str(table))
    logger.info("Total window aggregates processed: " + str(stats['windows']))

def display_joined_data():
    """Display a table of recent joined sensor data"""
    if not recent_joins:
        logger.info("No recent joined data to display")
        return
    
    logger.info(f"=== JOINED SENSOR DATA (Last {len(recent_joins)}) ===")
    
    table = PrettyTable()
    table.field_names = [
        "Time", 
        "Location", 
        "Temperature (°C)", 
        "Humidity (%)", 
        "Pressure (hPa)"
    ]
    
    for joined in recent_joins:
        timestamp = datetime.fromisoformat(joined['timestamp']).strftime("%H:%M:%S")
        table.add_row([
            timestamp,
            joined['location'],
            f"{joined.get('temperature', 'N/A'):.1f}",
            f"{joined.get('humidity', 'N/A'):.1f}",
            f"{joined.get('pressure', 'N/A'):.1f}"
        ])
    
    print("\n" + str(table))
    logger.info("Total joins processed: " + str(stats['joins']))

def process_anomaly_alert(message_data):
    """Process an incoming anomaly alert"""
    recent_anomalies.append(message_data)
    stats['anomalies'] += 1
    
    # Keep only the 10 most recent alerts
    if len(recent_anomalies) > 10:
        recent_anomalies.pop(0)
    
    # Display alerts immediately and then every 5 seconds
    current_time = datetime.now()
    if (current_time - last_display['anomalies']).total_seconds() >= 5:
        display_anomaly_alerts()
        last_display['anomalies'] = current_time

def process_window_aggregate(message_data):
    """Process an incoming window aggregate"""
    location = message_data['location']
    recent_windows[location] = message_data
    stats['windows'] += 1
    
    # Display window data every 10 seconds
    current_time = datetime.now()
    if (current_time - last_display['windows']).total_seconds() >= 10:
        display_window_aggregates()
        last_display['windows'] = current_time

def process_joined_data(message_data):
    """Process incoming joined data"""
    recent_joins.append(message_data)
    stats['joins'] += 1
    
    # Keep only the 10 most recent joins
    if len(recent_joins) > 10:
        recent_joins.pop(0)
    
    # Display joined data every 7 seconds
    current_time = datetime.now()
    if (current_time - last_display['joins']).total_seconds() >= 7:
        display_joined_data()
        last_display['joins'] = current_time

# Main processing loop
try:
    logger.info("Starting result consumer...")
    
    # Enforce display of all report types at startup after receiving initial data
    last_display = {
        'anomalies': datetime.min,
        'windows': datetime.min,
        'joins': datetime.min
    }
    
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
                
                # Process based on topic
                if topic == 'anomaly-alerts':
                    process_anomaly_alert(message_data)
                elif topic == 'window-aggregates':
                    process_window_aggregate(message_data)
                elif topic == 'joined-sensor-data':
                    process_joined_data(message_data)
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
        
        # Give the CPU a break
        time.sleep(0.01)

except KeyboardInterrupt:
    logger.info("Interrupted by user, shutting down...")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
finally:
    # Close the consumer
    consumer.close()
    logger.info("Result consumer stopped.") 