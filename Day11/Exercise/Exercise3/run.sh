#!/bin/bash

echo "Starting Anomaly Detection Pipeline"

# Create Python virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start Docker containers
echo "Starting Docker services (Kafka, Zookeeper, Flink, Redis)..."
docker-compose down
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Create Kafka topics
echo "Creating Kafka topics..."
docker exec kafka kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9096 \
    --topic transactions \
    --partitions 1 \
    --replication-factor 1

docker exec kafka kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9096 \
    --topic anomalies \
    --partitions 1 \
    --replication-factor 1

# Build the Flink CEP job
echo "Building Flink CEP job..."
cd flink-cep-job
mvn clean package
cd ..

# Submit the Flink job
echo "Submitting Flink job to the JobManager..."
docker cp flink-cep-job/target/flink-cep-job-1.0-SNAPSHOT.jar jobmanager:/opt/flink/usrlib/
docker exec jobmanager flink run -d -c com.anomaly.AnomalyDetectionJob /opt/flink/usrlib/flink-cep-job-1.0-SNAPSHOT.jar

# Start the transaction producer
echo "Starting transaction producer..."
python code/transaction_producer.py
