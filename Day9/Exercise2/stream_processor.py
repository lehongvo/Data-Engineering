import json
import time
from datetime import datetime
from kafka import KafkaConsumer
from collections import defaultdict

consumer = KafkaConsumer(
    'event-stream',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='stream-processor'
)

print('Stream Processor started. Aggregating events per minute...')

# Storage for event counts
event_counts = defaultdict(lambda: defaultdict(int))
minute_aggregates = defaultdict(int)

# Last minute processed
last_minute = None

try:
    for message in consumer:
        # Get the event data
        event = message.value
        
        # Parse timestamp
        timestamp = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S')
        minute_key = timestamp.strftime('%Y-%m-%d %H:%M')
        
        # Count events by type per minute
        event_type = event['event_type']
        event_counts[minute_key][event_type] += 1
        minute_aggregates[minute_key] += 1
        
        # If we've moved to a new minute, print summary of the last complete minute
        if last_minute and last_minute != minute_key:
            print(f"\n=== MINUTE SUMMARY: {last_minute} ===")
            print(f"Total events: {minute_aggregates[last_minute]}")
            print("Events by type:")
            for event_type, count in event_counts[last_minute].items():
                print(f"  - {event_type}: {count}")
            print("=" * 40)
        
        # Update last minute
        last_minute = minute_key
        
        # Print current event
        print(f"Processing: {event['event_type']} event at {event['timestamp']}")
        
except KeyboardInterrupt:
    print('Stream Processor stopped.')
finally:
    consumer.close() 