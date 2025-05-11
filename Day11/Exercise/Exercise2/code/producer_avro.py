import json
import argparse
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

SCHEMA_REGISTRY_URL = 'http://localhost:8081'
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'users-avro'

# Load both schema versions
value_schema_v1 = avro.load('./schema/user.avsc')
value_schema_v2 = avro.load('./schema/user_v2.avsc')

def create_producer(schema_version=1):
    schema = value_schema_v1 if schema_version == 1 else value_schema_v2
    return AvroProducer(
        {
            'bootstrap.servers': KAFKA_BROKER,
            'schema.registry.url': SCHEMA_REGISTRY_URL
        },
        default_value_schema=schema
    )

def produce_user(name, age, email=None, address=None, phone=None, schema_version=1):
    producer = create_producer(schema_version)
    
    if schema_version == 1:
        value = {
            "name": name,
            "age": age,
            "email": email,
            "schema_version": 1
        }
    else:
        value = {
            "name": name,
            "age": age,
            "email": email,
            "address": address,
            "phone": phone,
            "schema_version": 2
        }
    
    producer.produce(topic=TOPIC, value=value)
    producer.flush()

def main():
    parser = argparse.ArgumentParser(description='Avro Producer with Schema Version')
    parser.add_argument('--schema-version', type=int, choices=[1, 2], default=1,
                      help='Schema version to use (1 or 2)')
    args = parser.parse_args()

    if args.schema_version == 1:
        print("Producing messages with V1 schema...")
        users = [
            ("Alice", 30, "alice@example.com"),
            ("Bob", 25, None),
            ("Charlie", 28, "charlie@example.com")
        ]
        for name, age, email in users:
            produce_user(name, age, email, schema_version=1)
    else:
        print("Producing messages with V2 schema...")
        users = [
            ("David", 35, "david@example.com", "123 Main St", "555-0123"),
            ("Eve", 27, "eve@example.com", "456 Oak Ave", None),
            ("Frank", 32, None, None, "555-9876")
        ]
        for name, age, email, address, phone in users:
            produce_user(name, age, email, address, phone, schema_version=2)
    
    print("Produced Avro messages to Kafka!")

if __name__ == "__main__":
    main()
