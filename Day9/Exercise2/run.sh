#!/bin/bash

echo "=============================="
echo "Run Kafka Stream Processing Demo"
echo "=============================="

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
    echo "Error: docker-compose.yml not found. Please run from the Exercise2 directory."
    exit 1
  fi
else
  echo "Kafka and Zookeeper containers are already running."
fi

echo "- Stream Processor will run in background (logs saved to stream_processor.log)"
echo "- Event Producer will run in foreground (logs saved to producer.log)"
echo "- To stop, press Ctrl+C"
echo "=============================="

# Clear any existing log files
> stream_processor.log
> producer.log

# Run stream processor in background
python3 stream_processor.py > stream_processor.log 2>&1 &
PROCESSOR_PID=$!
echo "Stream Processor is running (PID: $PROCESSOR_PID), log: stream_processor.log"

# Run producer in foreground, but capture logs
python3 producer.py 2>&1 | tee producer.log

# When producer stops, stop processor as well
kill $PROCESSOR_PID 2>/dev/null
wait $PROCESSOR_PID 2>/dev/null 