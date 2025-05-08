import time
import random
import json
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'event-stream'

print('Event Producer started. Sending random event data...')

# Event types for simulation
EVENT_TYPES = ['click', 'view', 'purchase', 'login', 'logout']
USER_IDS = list(range(1, 21))  # 20 users

try:
    while True:
        # Generate random event data
        event = {
            'event_id': random.randint(10000, 99999),
            'event_type': random.choice(EVENT_TYPES),
            'user_id': random.choice(USER_IDS),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp_ms': int(time.time() * 1000)
        }
        
        producer.send(topic, event)
        print(f"Sent: {event}")
        
        # Random delay between events (0.1 to 0.5 seconds)
        time.sleep(random.uniform(0.1, 0.5))
except KeyboardInterrupt:
    print('Event Producer stopped.')
finally:
    producer.close() 