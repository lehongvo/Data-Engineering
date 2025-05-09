#!/usr/bin/env python3
from confluent_kafka import Consumer, Producer, KafkaException
import json
import sys
import time
import os
import datetime
import socket
from collections import defaultdict

# Configuration for 5-minute window in milliseconds
WINDOW_SIZE_MS = 5  # 5 s
ABNORMAL_THRESHOLD = 30.0  # Celsius

class TemperatureWindow:
    """Class to manage windowed temperature data."""
    def __init__(self, window_size_ms):
        self.window_size_ms = window_size_ms
        self.sensors = defaultdict(list)
    
    def add_reading(self, sensor_id, temperature, timestamp_str):
        """Add a temperature reading to the appropriate window."""
        try:
            # Parse the ISO timestamp
            timestamp = datetime.datetime.fromisoformat(timestamp_str)
            timestamp_ms = int(timestamp.timestamp() * 1000)
            
            # Add to sensor's readings
            self.sensors[sensor_id].append({
                'temperature': temperature,
                'timestamp_ms': timestamp_ms
            })
            
            # Prune old readings outside the window
            self._prune_old_readings(sensor_id)
            
            return True
        except Exception as e:
            print(f"Error processing timestamp {timestamp_str}: {e}")
            return False
    
    def _prune_old_readings(self, sensor_id):
        """Remove readings that are outside the current window."""
        if sensor_id not in self.sensors:
            return
            
        current_time_ms = int(datetime.datetime.now().timestamp() * 1000)
        window_start_ms = current_time_ms - self.window_size_ms
        
        self.sensors[sensor_id] = [
            reading for reading in self.sensors[sensor_id]
            if reading['timestamp_ms'] >= window_start_ms
        ]
    
    def get_average_temperature(self, sensor_id=None):
        """
        Calculate average temperature for a sensor or all sensors.
        Returns a dictionary of sensor_id -> average_temp
        """
        result = {}
        
        if sensor_id:
            # For specific sensor
            self._prune_old_readings(sensor_id)
            readings = self.sensors[sensor_id]
            if readings:
                avg_temp = sum(r['temperature'] for r in readings) / len(readings)
                result[sensor_id] = round(avg_temp, 1)
        else:
            # For all sensors
            for sid in list(self.sensors.keys()):
                self._prune_old_readings(sid)
                readings = self.sensors[sid]
                if readings:
                    avg_temp = sum(r['temperature'] for r in readings) / len(readings)
                    result[sid] = round(avg_temp, 1)
        
        return result

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
        log_to_file('log/processor.log', f'ERROR: Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
        log_to_file('log/processor.log', f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def main():
    # Ensure log directory exists
    os.makedirs('log', exist_ok=True)
    
    log_to_file('log/processor.log', '--- Temperature Processor Started ---')
    
    # Log hostname and connection details for debugging
    hostname = socket.gethostname()
    log_to_file('log/processor.log', f'Hostname: {hostname}')
    log_to_file('log/processor.log', f'Trying to connect to Kafka broker at localhost:9094')
    
    # Create temperature window tracker
    temp_window = TemperatureWindow(WINDOW_SIZE_MS)
    
    # Last time we computed averages
    last_avg_time = 0
    
    # Consumer configuration
    conf_consumer = {
        'bootstrap.servers': 'localhost:9094',
        'group.id': 'temperature-processor',
        'auto.offset.reset': 'earliest',
        'session.timeout.ms': 10000,
        'heartbeat.interval.ms': 3000,
        'security.protocol': 'PLAINTEXT',
        'enable.auto.commit': True,
        'auto.commit.interval.ms': 5000,
        'socket.timeout.ms': 30000,
        'socket.keepalive.enable': True,
        'reconnect.backoff.ms': 50,
        'reconnect.backoff.max.ms': 1000
    }

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
        # Create Consumer and Producer instances
        print("Creating Kafka consumer and producer...")
        log_to_file('log/processor.log', 'Creating Kafka consumer and producer...')
        
        consumer = Consumer(conf_consumer)
        producer = Producer(conf_producer)
        
        print("Successfully created Kafka consumer and producer")
        log_to_file('log/processor.log', 'Successfully created Kafka consumer and producer')

        # Subscribe to the input topic
        consumer.subscribe(['temperature-readings'])
        log_to_file('log/processor.log', 'Subscribed to temperature-readings topic')

        print("Starting Temperature Processor Application:")
        print("- Reading from 'temperature-readings'")
        print("- Writing averages to 'temperature-averages' (5-minute windows)")
        print("- Writing alerts to 'temperature-alerts' (temperatures > 30°C)")
        print("Press Ctrl+C to exit")
        
        while True:
            # Poll for messages with a timeout of 1.0 second
            msg = consumer.poll(1.0)
            
            if msg is None:
                # No message received, continue polling
                
                # Check if it's time to compute averages (every 30 seconds)
                current_time = int(time.time())
                if current_time - last_avg_time >= 30:
                    averages = temp_window.get_average_temperature()
                    
                    if averages:
                        # Create message with timestamp
                        avg_message = {
                            'timestamp': datetime.datetime.now().isoformat(),
                            'window_size_minutes': 5,
                            'averages': averages
                        }
                        
                        # Produce to averages topic
                        avg_json = json.dumps(avg_message)
                        producer.produce('temperature-averages', 
                                        avg_json.encode('utf-8'), 
                                        callback=delivery_report)
                        
                        # Log the averages
                        print(f"Produced 5-minute averages: {avg_json}")
                        log_to_file('log/processor.log', f'Produced 5-minute averages: {avg_json}')
                        
                        # Update last average time
                        last_avg_time = current_time
                    
                    # Flush the producer
                    producer.flush(timeout=1.0)
                
                continue
                
            if msg.error():
                # Handle error
                error_msg = f"Consumer error: {msg.error()}"
                print(error_msg)
                log_to_file('log/processor.log', f'ERROR: {error_msg}')
                continue
                
            try:
                # Parse the JSON message
                value = msg.value().decode('utf-8')
                data = json.loads(value)
                
                # Log the received message
                log_to_file('log/processor.log', f'Received: {value}')
                
                # Extract fields
                sensor_id = data.get('sensorId')
                temperature = data.get('temperature')
                timestamp = data.get('timestamp')
                
                if not all([sensor_id, temperature, timestamp]):
                    print(f"Missing required fields in message: {value}")
                    log_to_file('log/processor.log', f'ERROR: Missing required fields in message: {value}')
                    continue
                
                # Add to window tracker
                temp_window.add_reading(sensor_id, temperature, timestamp)
                
                # Check for abnormal temperature
                if temperature > ABNORMAL_THRESHOLD:
                    # Create alert message
                    alert_message = {
                        'timestamp': datetime.datetime.now().isoformat(),
                        'sensorId': sensor_id,
                        'temperature': temperature,
                        'threshold': ABNORMAL_THRESHOLD,
                        'message': f"Abnormal temperature detected: {temperature}°C exceeds threshold of {ABNORMAL_THRESHOLD}°C"
                    }
                    
                    # Produce to alerts topic
                    alert_json = json.dumps(alert_message)
                    producer.produce('temperature-alerts', 
                                   alert_json.encode('utf-8'), 
                                   callback=delivery_report)
                    
                    # Log the alert
                    print(f"ALERT! Abnormal temperature: {alert_json}")
                    log_to_file('log/processor.log', f'ALERT! Abnormal temperature: {alert_json}')
                
                # Flush the producer
                producer.flush(timeout=1.0)
                
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                log_to_file('log/processor.log', f'ERROR: Error decoding JSON: {e}')
            except Exception as e:
                print(f"Error processing message: {e}")
                log_to_file('log/processor.log', f'ERROR: Error processing message: {e}')
                
    except KafkaException as e:
        print(f"Kafka error: {e}")
        log_to_file('log/processor.log', f'ERROR: Kafka error: {e}')
    except KeyboardInterrupt:
        print("Closing consumer and producer...")
        log_to_file('log/processor.log', '--- Temperature Processor Stopped ---')
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_to_file('log/processor.log', f'ERROR: Unexpected error: {e}')
    finally:
        # Clean up before exit
        try:
            if 'consumer' in locals():
                consumer.close()
        except Exception as e:
            print(f"Error closing consumer: {e}")
            log_to_file('log/processor.log', f'ERROR: Error closing consumer: {e}')
        
if __name__ == '__main__':
    main() 