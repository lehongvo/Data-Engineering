#!/bin/bash

echo "=========================================="
echo "Kafka Consumer Groups Demo"
echo "=========================================="

# Check if Docker is running
echo "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running. Please start Docker first."
  exit 1
fi

# Check if Kafka containers are running
KAFKA_RUNNING=$(docker ps --filter "name=kafka" --format "{{.Names}}" | wc -l)
ZOOKEEPER_RUNNING=$(docker ps --filter "name=zookeeper" --format "{{.Names}}" | wc -l)

# If containers are not running, start them
if [ "$KAFKA_RUNNING" -eq 0 ] || [ "$ZOOKEEPER_RUNNING" -eq 0 ]; then
  echo "Kafka or Zookeeper containers are not running. Starting them now..."
  
  # Check if the docker-compose file exists
  if [ -f "docker-compose.yml" ]; then
    docker-compose down 2>/dev/null  # Stop any existing containers
    docker-compose up -d
    
    echo "Waiting for Kafka to start up (30 seconds)..."
    sleep 30  # Give Kafka time to start up
  else
    echo "Error: docker-compose.yml not found. Please run from the Exercise3 directory."
    exit 1
  fi
else
  echo "Kafka and Zookeeper containers are already running."
fi

# Clear any existing log files
> transaction_producer.log
> consumer_group1.log
> consumer_group2.log

echo "Starting consumers and producer..."
echo "- Consumer Group 1 (Revenue Aggregator) will run in background (logs to consumer_group1.log)"
echo "- Consumer Group 2 (User Behavior Analyzer) will run in background (logs to consumer_group2.log)"
echo "- Transaction Producer will run in foreground (logs to transaction_producer.log)"
echo "- To stop all processes, press Ctrl+C"
echo "=========================================="

# Run consumer group 1 in background
python3 consumer_group1.py > consumer_group1.log 2>&1 &
CONSUMER1_PID=$!
echo "Consumer Group 1 is running (PID: $CONSUMER1_PID)"

# Run consumer group 2 in background
python3 consumer_group2.py > consumer_group2.log 2>&1 &
CONSUMER2_PID=$!
echo "Consumer Group 2 is running (PID: $CONSUMER2_PID)"

# Run producer in foreground
python3 transaction_producer.py 2>&1 | tee transaction_producer.log

# When producer stops, stop consumers
echo "Shutting down consumers..."
kill $CONSUMER1_PID $CONSUMER2_PID 2>/dev/null
wait $CONSUMER1_PID 2>/dev/null
wait $CONSUMER2_PID 2>/dev/null 