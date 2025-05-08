# Exercise 2: Kafka Stream Processing with Aggregation

## Description
This exercise demonstrates a real-time stream processing application using Apache Kafka, where we:
1. Generate random event data (clicks, views, purchases, etc.)
2. Process the event stream in real-time
3. Perform aggregation operations to count events per minute, by type

## Requirements
- Kafka running on `localhost:9092`
- Python 3 with the `kafka-python` library

Install dependencies:
```bash
pip install kafka-python
```

## Running the Application
First, make sure your Kafka is running:
```bash
# From the Exercise2 directory
docker-compose up -d
```

### Method 1: Using the run script
```bash
chmod +x run.sh
./run.sh
```

### Method 2: Running components separately
#### Terminal 1: Run the Stream Processor
```bash
python3 stream_processor.py
```

#### Terminal 2: Run the Event Producer
```bash
python3 producer.py
```

## Expected Results
- The producer will generate random events with different types and timestamps
- The stream processor will:
  - Track events in real-time
  - Group events by minute
  - Calculate per-minute statistics by event type
  - Print summaries when a minute completes

## Key Concepts Demonstrated
- Real-time data processing
- Stateful stream processing
- Time-based windowing (by minute)
- Event aggregation

## Notes
- Press `Ctrl+C` to stop either component
- For a real production system, consider using Kafka Streams API or Apache Flink for more powerful stream processing capabilities 