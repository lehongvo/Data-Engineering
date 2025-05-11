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

def produce_invalid_user():
    # Invalid cases: missing 'name', 'age' as string instead of int, or 'name' is None
    invalid_users = [
        {"age": "thirty", "email": "invalid1@example.com"},
        {"name": "NoAge"},
        {"name": None, "age": 22, "email": "invalid2@example.com"}
    ]
    for value in invalid_users:
        try:
            producer.produce(topic=TOPIC, value=value)
            producer.flush()
            print(f"Produced invalid message: {value}")
        except Exception as e:
            print(f"Error producing invalid message {value}: {e}")

if __name__ == "__main__":
    produce_invalid_user()
    print("Finished producing invalid Avro messages!") 