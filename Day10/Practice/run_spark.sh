#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[SPARK]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Make the script directory the working directory
cd "$(dirname "$0")"

# Check if Python and Spark dependencies are installed
print_step "Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if PySpark is installed
if ! python3 -c "import pyspark" &> /dev/null; then
    print_error "PySpark is not installed. Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Failed to install required packages."
        exit 1
    fi
fi

# Create necessary directories if they don't exist
print_step "Creating necessary directories..."
mkdir -p output/address_volume output/contract_interactions output/gas_trends
mkdir -p checkpoint/address_volume checkpoint/contract_interactions checkpoint/gas_trends
mkdir -p logs

# Check if Kafka is running
print_step "Checking if Kafka is running..."
if ! nc -z localhost 9092 &> /dev/null; then
    print_error "Kafka doesn't seem to be running on localhost:9092."
    print_message "Starting Kafka and Zookeeper..."
    
    if [ -f "docker-compose.yml" ]; then
        docker-compose up -d
        sleep 15  # Wait for Kafka to start
    else
        print_error "docker-compose.yml not found. Please start Kafka manually."
        exit 1
    fi
fi

# Run the Spark streaming application
print_step "Starting Spark streaming application..."
python3 spark_streaming.py > logs/spark-streaming.log 2>&1 &
SPARK_PID=$!

# Check if Spark is running
sleep 5
if kill -0 $SPARK_PID 2>/dev/null; then
    print_message "Spark streaming application started successfully (PID: $SPARK_PID)"
    print_message "Log file: logs/spark-streaming.log"
    print_message "Use 'tail -f logs/spark-streaming.log' to view logs"
else
    print_error "Failed to start Spark streaming application."
    print_message "Check logs/spark-streaming.log for details."
    exit 1
fi

echo
print_message "Spark streaming is running in the background."
print_message "To stop the application, use: kill -SIGTERM $SPARK_PID"
print_message "Output will be saved to: output/address_volume, output/contract_interactions, output/gas_trends" 