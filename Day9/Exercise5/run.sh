#!/bin/bash

echo "======================================================"
echo "Exercise 5: Error Handling and Dead Letter Queues in Kafka"
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

# Ensure log directories exist
mkdir -p logs

# Install required Python libraries
echo "Installing required Python libraries..."
pip install kafka-python prettytable

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
chmod +x producer.py consumer.py dlq_consumer.py error_analytics.py

# Run programs in separate windows
echo "Starting system components..."
echo "1. Starting Error Analytics"
echo "2. Starting DLQ Consumer"
echo "3. Starting Main Consumer"
echo "4. Starting Producer (last to ensure consumers are ready)"
echo "======================================================"

# Clear old logs if they exist
> producer.log
> consumer.log
> dlq_consumer.log
> error_analytics.log

# Start components in background
echo "Starting error_analytics.py..."
./error_analytics.py > logs/error_analytics_stdout.log 2>&1 &
ERROR_ANALYTICS_PID=$!
sleep 2

echo "Starting dlq_consumer.py..."
./dlq_consumer.py > logs/dlq_consumer_stdout.log 2>&1 &
DLQ_CONSUMER_PID=$!
sleep 2

echo "Starting consumer.py..."
./consumer.py > logs/consumer_stdout.log 2>&1 &
CONSUMER_PID=$!
sleep 2

echo "Starting producer.py..."
./producer.py > logs/producer_stdout.log 2>&1 &
PRODUCER_PID=$!

echo "======================================================"
echo "All components have been started!"
echo ""
echo "To view logs:"
echo "- Producer log:        tail -f producer.log"
echo "- Consumer log:        tail -f consumer.log"
echo "- DLQ Consumer log:    tail -f dlq_consumer.log"
echo "- Error Analytics log: tail -f error_analytics.log"
echo ""
echo "PIDs of processes:"
echo "- Producer:        $PRODUCER_PID"
echo "- Consumer:        $CONSUMER_PID"
echo "- DLQ Consumer:    $DLQ_CONSUMER_PID"
echo "- Error Analytics: $ERROR_ANALYTICS_PID"
echo ""
echo "To stop the entire system, press Ctrl+C..."
echo "======================================================"

# Cleanup function when script is interrupted
cleanup() {
    echo "Stopping processes..."
    kill $PRODUCER_PID 2>/dev/null
    kill $CONSUMER_PID 2>/dev/null
    kill $DLQ_CONSUMER_PID 2>/dev/null
    kill $ERROR_ANALYTICS_PID 2>/dev/null
    
    echo "Stopping Docker containers..."
    docker-compose down
    
    echo "Cleanup complete."
    exit 0
}

# Catch Ctrl+C event
trap cleanup SIGINT SIGTERM

# Display combined logs
echo "Displaying logs (Press Ctrl+C to stop)..."
tail -f producer.log consumer.log dlq_consumer.log error_analytics.log 