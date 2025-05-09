#!/usr/bin/env python3
from confluent_kafka import Producer
import json
import random
import time
import datetime
import os
import argparse
import socket

# Sensor IDs for simulation
SENSOR_IDS = ["sensor-001", "sensor-002", "sensor-003", "sensor-004", "sensor-005"]

def get_timestamp():
    """Get current timestamp for logging."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_to_file(file_path, message):
    """Log message to file with timestamp."""
    with open(file_path, 'a') as f:
        f.write(f"[{get_timestamp()}] {message}\n")

def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result."""
    if err is not None:
        print(f'Message delivery failed: {err}')
        log_to_file('log/producer.log', f'ERROR: Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
        log_to_file('log/producer.log', f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def generate_temperature_reading(sensor_id=None, abnormal_chance=0.1):
    """Generate a simulated temperature reading."""
    if sensor_id is None:
        sensor_id = random.choice(SENSOR_IDS)
    
    # Decide if this should be an abnormal reading
    is_abnormal = random.random() < abnormal_chance
    
    # Normal temperatures between 18-28°C, abnormal above 30°C
    if is_abnormal:
        temperature = round(random.uniform(30.1, 40.0), 1)
    else:
        temperature = round(random.uniform(18.0, 28.0), 1)
    
    # Current timestamp in ISO format
    timestamp = datetime.datetime.now().isoformat()
    
    return {
        "sensorId": sensor_id,
        "temperature": temperature,
        "timestamp": timestamp,
        "unit": "Celsius"
    }

def main():
    parser = argparse.ArgumentParser(description='Temperature Sensor Data Producer')
    parser.add_argument('--interval', type=float, default=1.0, 
                        help='Time interval between generated readings in seconds')
    parser.add_argument('--abnormal-rate', type=float, default=0.1, 
                        help='Probability of generating abnormal temperature readings (0.0-1.0)')
    parser.add_argument('--count', type=int, default=0, 
                        help='Number of readings to generate (0 for continuous)')
    args = parser.parse_args()
    
    # Ensure log directory exists
    os.makedirs('log', exist_ok=True)
    
    log_to_file('log/producer.log', '--- Temperature Producer Started ---')
    
    # Log hostname and connection details for debugging
    hostname = socket.gethostname()
    log_to_file('log/producer.log', f'Hostname: {hostname}')
    log_to_file('log/producer.log', f'Trying to connect to Kafka broker at localhost:9094')
    
    # Producer configuration
    conf_producer = {
        'bootstrap.servers': 'localhost:9094',
        'security.protocol': 'PLAINTEXT',
        'queue.buffering.max.messages': 10000,
        'queue.buffering.max.ms': 100,
        'retry.backoff.ms': 250,
        'retries': 5,
        'socket.timeout.ms': 30000,
        'socket.keepalive.enable': True,
        'reconnect.backoff.ms': 50,
        'reconnect.backoff.max.ms': 1000
    }

    try:
        # Create Producer instance
        print("Creating Kafka producer...")
        log_to_file('log/producer.log', 'Creating Kafka producer...')
        
        producer = Producer(conf_producer)
        
        print("Successfully created Kafka producer")
        log_to_file('log/producer.log', 'Successfully created Kafka producer')

        print(f"Starting Temperature Data Producer")
        print(f"Sending to 'temperature-readings' topic at interval of {args.interval} seconds")
        print(f"Abnormal temperature rate: {args.abnormal_rate * 100}%")
        if args.count > 0:
            print(f"Will generate {args.count} readings and then exit")
        else:
            print("Running continuously. Press Ctrl+C to exit")
        
        reading_count = 0
        
        while args.count == 0 or reading_count < args.count:
            # Generate a temperature reading
            reading = generate_temperature_reading(abnormal_chance=args.abnormal_rate)
            
            # Convert to JSON
            message = json.dumps(reading)
            
            # Log the reading
            log_msg = f"Generated: {message}"
            print(log_msg)
            log_to_file('log/producer.log', log_msg)
            
            # Produce the message
            producer.produce('temperature-readings', 
                           message.encode('utf-8'), 
                           callback=delivery_report)
            
            # Flush the producer to deliver any pending messages
            producer.flush(timeout=1.0)
            
            # Increment count if needed
            if args.count > 0:
                reading_count += 1
                
            # Wait for the specified interval
            time.sleep(args.interval)
                
    except KeyboardInterrupt:
        print("Producer shutting down...")
        log_to_file('log/producer.log', '--- Temperature Producer Stopped ---')
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_to_file('log/producer.log', f'ERROR: Unexpected error: {e}')
    finally:
        # Ensure all messages are delivered before exiting
        if 'producer' in locals():
            producer.flush(timeout=5.0)
        
if __name__ == '__main__':
    main() 