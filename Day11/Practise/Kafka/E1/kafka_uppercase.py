from confluent_kafka import Consumer, Producer, KafkaException
import sys
import time
import os
import datetime
import socket

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
        log_to_file('log/output.log', f'ERROR: Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
        log_to_file('log/output.log', f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def main():
    # Ensure log directory exists
    os.makedirs('log', exist_ok=True)
    
    log_to_file('log/output.log', '--- Kafka Streams Application Started ---')
    
    # Log hostname and connection details for debugging
    hostname = socket.gethostname()
    log_to_file('log/output.log', f'Hostname: {hostname}')
    log_to_file('log/output.log', f'Trying to connect to Kafka broker at localhost:9094')
    
    # Consumer configuration
    conf_consumer = {
        'bootstrap.servers': 'localhost:9094',
        'group.id': 'uppercase-app',
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
        log_to_file('log/output.log', 'Creating Kafka consumer and producer...')
        
        consumer = Consumer(conf_consumer)
        producer = Producer(conf_producer)
        
        print("Successfully created Kafka consumer and producer")
        log_to_file('log/output.log', 'Successfully created Kafka consumer and producer')

        # Subscribe to the input topic
        consumer.subscribe(['input-topic'])
        log_to_file('log/output.log', 'Subscribed to input-topic')

        print("Starting Kafka Streams application: Input-to-Uppercase")
        print("Reading from 'input-topic' and writing to 'output-topic'")
        print("Press Ctrl+C to exit")
        
        while True:
            # Poll for messages with a timeout of 1.0 second
            msg = consumer.poll(1.0)
            
            if msg is None:
                # No message received, continue polling
                continue
                
            if msg.error():
                # Handle error
                error_msg = f"Consumer error: {msg.error()}"
                print(error_msg)
                log_to_file('log/output.log', f'ERROR: {error_msg}')
                continue
                
            try:
                # Get the message value and convert to string
                value = msg.value().decode('utf-8')
                log_to_file('log/input.log', f'Received: {value}')
                print(f"Received message: {value}")
                
                # Transform the message to uppercase
                transformed_value = value.upper()
                log_to_file('log/output.log', f'Transformed: {value} -> {transformed_value}')
                print(f"Transformed message: {transformed_value}")
                
                # Produce the transformed message to the output topic
                producer.produce('output-topic', 
                                transformed_value.encode('utf-8'), 
                                callback=delivery_report)
                
                # Flush the producer to deliver any pending messages
                producer.flush(timeout=5.0)
            except Exception as e:
                print(f"Error processing message: {e}")
                log_to_file('log/output.log', f'ERROR: Error processing message: {e}')
                
    except KafkaException as e:
        print(f"Kafka error: {e}")
        log_to_file('log/output.log', f'ERROR: Kafka error: {e}')
    except KeyboardInterrupt:
        print("Closing consumer and producer...")
        log_to_file('log/output.log', '--- Kafka Streams Application Stopped ---')
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_to_file('log/output.log', f'ERROR: Unexpected error: {e}')
    finally:
        # Clean up before exit
        try:
            if 'consumer' in locals():
                consumer.close()
        except Exception as e:
            print(f"Error closing consumer: {e}")
            log_to_file('log/output.log', f'ERROR: Error closing consumer: {e}')
        
if __name__ == '__main__':
    main()
