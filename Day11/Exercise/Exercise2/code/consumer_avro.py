from confluent_kafka.avro import AvroConsumer

SCHEMA_REGISTRY_URL = 'http://localhost:8081'
KAFKA_BROKER = 'localhost:9095'
TOPIC = 'users-avro'

consumer = AvroConsumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'avro-consumer-group',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': SCHEMA_REGISTRY_URL
})

consumer.subscribe([TOPIC])

print("Waiting for messages...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        print(f"Received message: {msg.value()}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
