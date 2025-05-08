#!/bin/bash

echo "======================================================"
echo "Exercise 6: Kafka Streams for Real-time Processing"
echo "======================================================"

# Check Docker
echo "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running. Please start Docker first."
  exit 1
fi

# Stop old containers from other exercises
echo "Stopping old containers from previous exercises (if any)..."
docker-compose down 2>/dev/null
docker-compose -f ../Exercise1/docker-compose.yml down 2>/dev/null 
docker-compose -f ../Exercise2/docker-compose.yml down 2>/dev/null
docker-compose -f ../Exercise3/docker-compose.yml down 2>/dev/null
docker-compose -f ../Exercise4/docker-compose.yml down 2>/dev/null
docker-compose -f ../Exercise5/docker-compose.yml down 2>/dev/null

# Ensure log directories exist
mkdir -p logs

# Install required Python libraries
echo "Installing required Python libraries..."
pip install confluent-kafka prettytable kafka-python

# Start Docker Compose
echo "Starting Kafka containers..."
docker-compose up -d

echo "Waiting for Kafka to start (30 seconds)..."
sleep 30

# Check if Kafka is ready
echo "Checking if Kafka is ready..."
if ! docker-compose ps | grep -q "kafka.*Up"; then
  echo "Error: Kafka failed to start. Check logs:"
  docker-compose logs kafka
  exit 1
fi

echo "Kafka is ready!"
echo "======================================================"

# Ensure Python files are executable
chmod +x sensor_producer.py stream_processor.py result_consumer.py

# Clear old logs if they exist
> sensor_producer.log
> stream_processor.log
> result_consumer.log

echo "======================================================"
echo "Starting system components..."
echo "1. Starting Stream Processor (to process the data streams)"
echo "2. Starting Result Consumer (to display the results)"
echo "3. Starting Sensor Producer (to generate test data)"
echo "======================================================"

# Start components in background
echo "Starting stream_processor.py..."
./stream_processor.py > logs/stream_processor_stdout.log 2>&1 &
STREAM_PROCESSOR_PID=$!
sleep 2

echo "Starting result_consumer.py..."
./result_consumer.py > logs/result_consumer_stdout.log 2>&1 &
RESULT_CONSUMER_PID=$!
sleep 2

echo "Starting sensor_producer.py..."
./sensor_producer.py > logs/sensor_producer_stdout.log 2>&1 &
SENSOR_PRODUCER_PID=$!

echo "======================================================"
echo "All components have been started!"
echo ""
echo "To view logs:"
echo "- Sensor Producer log:   tail -f sensor_producer.log"
echo "- Stream Processor log:  tail -f stream_processor.log"
echo "- Result Consumer log:   tail -f result_consumer.log"
echo ""
echo "PIDs of processes:"
echo "- Stream Processor:    $STREAM_PROCESSOR_PID"
echo "- Result Consumer:     $RESULT_CONSUMER_PID"
echo "- Sensor Producer:     $SENSOR_PRODUCER_PID"
echo ""
echo "To stop the entire system, press Ctrl+C..."
echo "======================================================"

# Cleanup function when script is interrupted
cleanup() {
    echo "Stopping processes..."
    kill $STREAM_PROCESSOR_PID 2>/dev/null
    kill $RESULT_CONSUMER_PID 2>/dev/null
    kill $SENSOR_PRODUCER_PID 2>/dev/null
    
    echo "Stopping Docker containers..."
    docker-compose down
    
    echo "Cleanup complete."
    exit 0
}

# Catch Ctrl+C event
trap cleanup SIGINT SIGTERM

# Display combined logs
echo "Displaying logs (Press Ctrl+C to stop)..."
tail -f sensor_producer.log stream_processor.log result_consumer.log 