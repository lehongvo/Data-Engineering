#!/bin/bash

echo "====================================================="
echo "Kafka Connect: Mock PostgreSQL to MongoDB Demo"
echo "====================================================="

# Check if Docker is running
echo "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running. Please start Docker first."
  exit 1
fi

# Ensure directories exist
mkdir -p connect-config
mkdir -p logs

# Stop any existing containers from previous exercises
echo "Stopping any existing containers from previous exercises..."
docker-compose down 2>/dev/null
docker-compose -f ../Exercise1/docker-compose.yml down 2>/dev/null
docker-compose -f ../Exercise2/docker-compose.yml down 2>/dev/null
docker-compose -f ../Exercise3/docker-compose.yml down 2>/dev/null

echo "Starting Kafka Connect environment..."
echo "This will start Zookeeper, Kafka, Kafka Connect, PostgreSQL, and MongoDB"
echo "====================================================="

# Start all services
docker-compose up -d

echo "Waiting for services to initialize (30 seconds)..."
sleep 30  # Increased wait time to ensure all services are fully ready

# Check if services are running
echo "Checking if all services are running..."
KAFKA_RUNNING=$(docker-compose ps | grep kafka | grep -v kafka-connect | grep Up | wc -l)
CONNECT_RUNNING=$(docker-compose ps | grep kafka-connect | grep Up | wc -l)
POSTGRES_RUNNING=$(docker-compose ps | grep postgres | grep Up | wc -l)
MONGODB_RUNNING=$(docker-compose ps | grep mongodb | grep Up | wc -l)

if [ "$KAFKA_RUNNING" -eq 0 ] || [ "$POSTGRES_RUNNING" -eq 0 ] || [ "$MONGODB_RUNNING" -eq 0 ] || [ "$CONNECT_RUNNING" -eq 0 ]; then
  echo "Error: Some services failed to start. Please check docker-compose logs."
  exit 1
fi

echo "All services are running!"
echo "====================================================="

# Demonstrate data flow
echo "Demonstration of data flow:"
echo "1. Mock source connector generates sample PostgreSQL-like data"
echo "2. Data is streamed to Kafka topics"
echo "3. Mock sink connector simulates writing to MongoDB"
echo "====================================================="

# Setup logs for monitoring
echo "====================================================="
echo "Setting up data flow monitoring..."

# Define log files
KAFKA_TOPICS_LOG="logs/kafka_topics.log"
KAFKA_MESSAGES_LOG="logs/kafka_messages.log"
CONNECTOR_STATUS_LOG="logs/connector_status.log"
SYSTEM_LOG="logs/system_flow.log"

# Clear old logs if they exist
> $KAFKA_TOPICS_LOG
> $KAFKA_MESSAGES_LOG
> $CONNECTOR_STATUS_LOG
> $SYSTEM_LOG

echo "========================================" | tee -a $SYSTEM_LOG
echo "Starting data flow logging: $(date)" | tee -a $SYSTEM_LOG
echo "========================================" | tee -a $SYSTEM_LOG

# Wait for Kafka Connect to start up completely
echo "Waiting 20 seconds for Kafka Connect to start up..." | tee -a $SYSTEM_LOG
sleep 20

# Check Kafka Connect status
echo "Checking Kafka Connect status..." | tee -a $CONNECTOR_STATUS_LOG
curl -s http://localhost:28083/ | tee -a $CONNECTOR_STATUS_LOG
echo "" | tee -a $CONNECTOR_STATUS_LOG

# List available connectors
echo "Available connector plugins:" | tee -a $CONNECTOR_STATUS_LOG
curl -s http://localhost:28083/connector-plugins | tee -a $CONNECTOR_STATUS_LOG
echo "" | tee -a $CONNECTOR_STATUS_LOG

# List active connectors
echo "Active connectors:" | tee -a $CONNECTOR_STATUS_LOG
curl -s http://localhost:28083/connectors | tee -a $CONNECTOR_STATUS_LOG
echo "" | tee -a $CONNECTOR_STATUS_LOG

# Check and log Kafka topics
echo "Current Kafka topics:" | tee -a $KAFKA_TOPICS_LOG
docker-compose exec -T kafka kafka-topics.sh --list --bootstrap-server kafka:9092 | tee -a $KAFKA_TOPICS_LOG
echo "----------------------------------------" | tee -a $KAFKA_TOPICS_LOG

# Wait for data to be processed
echo "Waiting 30 seconds for data to flow through Kafka..." | tee -a $SYSTEM_LOG
sleep 30

# Check for new data in topics
echo -e "\nChecking Kafka topics after waiting:" | tee -a $KAFKA_TOPICS_LOG
docker-compose exec -T kafka kafka-topics.sh --list --bootstrap-server kafka:9092 | tee -a $KAFKA_TOPICS_LOG

# Log topic details
docker-compose exec -T kafka kafka-topics.sh --describe --bootstrap-server kafka:9092 | tee -a $KAFKA_TOPICS_LOG

# Check topic content (if any)
echo -e "\nChecking messages in Kafka topics:" | tee -a $KAFKA_MESSAGES_LOG
TOPICS=$(docker-compose exec -T kafka kafka-topics.sh --list --bootstrap-server kafka:9092)
for topic in $TOPICS; do
  if [[ -n "$topic" && "$topic" != *"__"* ]]; then # Skip internal topics
    echo -e "\nMessages in topic '$topic':" | tee -a $KAFKA_MESSAGES_LOG
    docker-compose exec -T kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic $topic --from-beginning --max-messages 5 --timeout-ms 10000 | tee -a $KAFKA_MESSAGES_LOG 2>/dev/null || true
    echo "----------------------------------------" | tee -a $KAFKA_MESSAGES_LOG
  fi
done

# Summary of results
echo -e "\n========================================" | tee -a $SYSTEM_LOG
echo "Data flow logging results: $(date)" | tee -a $SYSTEM_LOG
echo "- Kafka topics log: $KAFKA_TOPICS_LOG" | tee -a $SYSTEM_LOG
echo "- Kafka messages log: $KAFKA_MESSAGES_LOG" | tee -a $SYSTEM_LOG 
echo "- Connector status log: $CONNECTOR_STATUS_LOG" | tee -a $SYSTEM_LOG
echo "========================================" | tee -a $SYSTEM_LOG

echo "Data flow monitoring completed. See log files in the 'logs/' directory."
echo "====================================================="

echo "====================================================="
echo "To monitor Kafka topics, run: "
echo "docker-compose exec kafka kafka-topics.sh --list --bootstrap-server kafka:9092"
echo ""
echo "To manually check messages in a topic, run:"
echo "docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic [TOPIC_NAME] --from-beginning"
echo "====================================================="

echo "To check Kafka Connect status:"
echo "curl -s http://localhost:28083/ | jq"
echo "====================================================="

echo "To stop the environment:"
echo "docker-compose down"
echo "=====================================================" 