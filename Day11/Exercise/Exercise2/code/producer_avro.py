import json
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

SCHEMA_REGISTRY_URL = 'http://localhost:8081'
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'users-avro'

value_schema = avro.load('./schema/user.avsc')

producer = AvroProducer(
    {
        'bootstrap.servers': KAFKA_BROKER,
        'schema.registry.url': SCHEMA_REGISTRY_URL
    },
    default_value_schema=value_schema
)

def produce_user(name, age, email=None):
    value = {"name": name, "age": age, "email": email}
    producer.produce(topic=TOPIC, value=value)
    producer.flush()

if __name__ == "__main__":
    users = [
        ("Alice", 30, "alice@example.com"),
        ("Bob", 25, None),
        ("Charlie", 28, "charlie@example.com")
    ]
    for name, age, email in users:
        produce_user(name, age, email)
    print("Produced Avro messages to Kafka!")
