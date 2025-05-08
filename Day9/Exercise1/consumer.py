from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'sensor-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print('Consumer started. Waiting for sensor data...')

try:
    for message in consumer:
        data = message.value
        print(f"Received: {data}")
except KeyboardInterrupt:
    print('Consumer stopped.')
finally:
    consumer.close() 