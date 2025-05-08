import time
import random
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'sensor-data'

print('Producer started. Sending random sensor data...')

try:
    while True:
        data = {
            'sensor_id': random.randint(1, 5),
            'temperature': round(random.uniform(20.0, 35.0), 2),
            'humidity': round(random.uniform(30.0, 70.0), 2),
            'timestamp': time.time()
        }
        producer.send(topic, data)
        print(f"Sent: {data}")
        time.sleep(1)
except KeyboardInterrupt:
    print('Producer stopped.')
finally:
    producer.close() 