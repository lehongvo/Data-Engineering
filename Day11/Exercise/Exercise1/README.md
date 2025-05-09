# Real-time Streaming Pipeline with Kafka, Flink and BigQuery

This pipeline processes clickstream data in real-time:
1. Kafka Producer sends clickstream data
2. Flink reads and processes data from Kafka
3. Processing results are stored in BigQuery

## Installation

### Requirements
- Docker and Docker Compose
- Python 3.7+
- Google Cloud Platform account (with BigQuery access)

### Install dependencies for Producer

```bash
pip install kafka-python
```

### Install dependencies for Flink Consumer

```bash
pip install apache-flink
```

## Deployment

### Step 1: Start the environment

```bash
docker-compose up -d
```

Check container status:
```bash
docker-compose ps
```

### Step 2: Run Kafka Producer

```bash
python code/producer/click_stream_producer.py
```

### Step 3: Submit Flink Job

```bash
# Copy Flink processor to container
docker cp code/consumer/flink_processor.py flink-jobmanager:/opt/flink/

# Access Flink container
docker exec -it flink-jobmanager /bin/bash

# Submit job
cd /opt/flink
python flink_processor.py
```

Or use the Flink Web UI:
- Access http://localhost:8081
- Upload JAR file and submit job

### Step 4: Connect to BigQuery

To connect with BigQuery:
1. Prepare Google Cloud credentials (service account key)
2. Uncomment the BigQuery sink section in the `flink_processor.py` file
3. Update project, dataset and table information for BigQuery
4. Resubmit the Flink job

## Monitoring

### Flink Dashboard
- Access http://localhost:8081 to view job information, task managers, ...

### Check Kafka Data

```bash
# List topics
docker exec -it kafka kafka-topics.sh --list --bootstrap-server kafka:9092

# Consume data from topic (for verification)
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic clickstream --from-beginning
```

### Monitor Processed Data in BigQuery
- Access Google Cloud Console > BigQuery
- Query data in the `clickstream_analytics` table

## Data Structure

### Clickstream Data (Kafka)
```json
{
  "event_id": "uuid",
  "user_id": "string",
  "page": "string",
  "action": "string",
  "device": "string",
  "timestamp": "string",
  "session_duration": "int",
  "referrer": "string"
}
```

### Processed Data (BigQuery)
```
- user_id (STRING)
- page (STRING)
- view_count (INT)
- avg_session_duration (FLOAT)
- last_activity (STRING)
```

## Error Handling

- Check logs:
```bash
docker-compose logs -f kafka
docker-compose logs -f flink-jobmanager
```

- If Kafka Producer cannot connect:
  - Check `bootstrap_servers` setting and ensure Kafka has started
  - Ensure port 9092 is open

- If Flink job fails:
  - Check logs and Flink UI
  - Ensure JAR files have been added with correct paths 