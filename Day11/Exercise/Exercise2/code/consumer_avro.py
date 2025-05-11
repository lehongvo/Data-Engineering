from confluent_kafka import avro
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
import json
import argparse

SCHEMA_REGISTRY_URL = 'http://localhost:8081'
KAFKA_BROKER = 'localhost:9092'  # Fixed port
TOPIC = 'users-avro'

def create_consumer():
    return AvroConsumer({
        'bootstrap.servers': KAFKA_BROKER,
        'schema.registry.url': SCHEMA_REGISTRY_URL,
        'group.id': 'user-consumer-group',
        'auto.offset.reset': 'earliest'
    })

def process_message(message, schema_version='all'):
    try:
        # Get the schema version from the message
        msg_schema_version = message.value().get('schema_version', 1)
        
        # Skip if we're filtering by schema version and it doesn't match
        if schema_version != 'all' and msg_schema_version != schema_version:
            return
        
        # Process based on schema version
        if msg_schema_version == 1:
            print(f"\nProcessing V1 schema message:")
            print(f"Name: {message.value()['name']}")
            print(f"Age: {message.value()['age']}")
            print(f"Email: {message.value()['email']}")
        else:
            print(f"\nProcessing V2 schema message:")
            print(f"Name: {message.value()['name']}")
            print(f"Age: {message.value()['age']}")
            print(f"Email: {message.value()['email']}")
            print(f"Address: {message.value().get('address')}")
            print(f"Phone: {message.value().get('phone')}")
            
    except Exception as e:
        print(f"Error processing message: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Avro Consumer with Schema Version')
    parser.add_argument('--schema-version', type=int, choices=[1, 2], default='all',
                      help='Schema version to process (1, 2, or all)')
    args = parser.parse_args()

    consumer = create_consumer()
    consumer.subscribe([TOPIC])
    
    print(f"Starting consumer for schema version: {args.schema_version}")
    
    try:
        while True:
            try:
                message = consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    print(f"Consumer error: {message.error()}")
                    continue
                
                process_message(message, args.schema_version)
                
            except SerializerError as e:
                print(f"Message deserialization failed: {str(e)}")
                continue
                
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
