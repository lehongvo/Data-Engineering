#!/bin/bash

# Setup function to initialize the environment
setup_environment() {
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt

    echo "Stopping Kafka and Zookeeper..."
    docker-compose down
    # Start Kafka and Zookeeper
    echo "Starting Kafka and Zookeeper..."
    docker-compose up -d

    # Wait for Kafka to be ready
    echo "Waiting for Kafka to be ready..."
    sleep 10

    # Check Kafka status
    echo "Checking Kafka status..."
    docker ps

    # Create topics
    echo "Creating temperature-readings topic..."
    docker exec -it e2-kafka kafka-topics --create --topic temperature-readings --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 || echo "Topic may already exist"

    echo "Creating temperature-averages topic..."
    docker exec -it e2-kafka kafka-topics --create --topic temperature-averages --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 || echo "Topic may already exist"

    echo "Creating temperature-alerts topic..."
    docker exec -it e2-kafka kafka-topics --create --topic temperature-alerts --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 || echo "Topic may already exist"

    # List topics to verify
    echo "Verifying topics..."
    docker exec -it e2-kafka kafka-topics --list --bootstrap-server kafka:9092

    # Setup logging information
    echo "Setting up logging..."
    mkdir -p log
    touch log/producer.log log/processor.log

    echo "Environment setup complete!"
    
    # Return to main menu after setup is complete
    sleep 2
    clear
    show_menu
}

# Run temperature producer
run_temperature_producer() {
    echo "Starting Temperature Producer..."
    python3 temperature_producer.py --interval 1.0 --abnormal-rate 0.15
}

# Run temperature processor
run_temperature_processor() {
    echo "Starting Temperature Processor Application..."
    python3 temperature_processor.py
}

# Run console consumer for averages
run_averages_consumer() {
    echo "Starting Kafka consumer for temperature-averages topic..."
    echo "Messages will be displayed here. Press Ctrl+C to exit."
    docker exec -it e2-kafka kafka-console-consumer --bootstrap-server localhost:9094 --topic temperature-averages --from-beginning
}

# Run console consumer for alerts
run_alerts_consumer() {
    echo "Starting Kafka consumer for temperature-alerts topic..."
    echo "Messages will be displayed here. Press Ctrl+C to exit."
    docker exec -it e2-kafka kafka-console-consumer --bootstrap-server localhost:9094 --topic temperature-alerts --from-beginning
}

# Run manual producer for temperature readings
run_manual_producer() {
    echo "Starting manual Kafka producer on temperature-readings topic..."
    echo "Enter JSON messages in the format: {\"sensorId\":\"sensor-001\",\"temperature\":25.5,\"timestamp\":\"$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")\",\"unit\":\"Celsius\"}"
    echo "Press Ctrl+C to exit."
    docker exec -it e2-kafka kafka-console-producer --broker-list localhost:9094 --topic temperature-readings
}

# Display menu and get user input
show_menu() {
    clear
    echo "========================================"
    echo "   TEMPERATURE MONITORING SYSTEM - E2   "
    echo "========================================"
    echo "Please select an option:"
    echo ""
    echo "1) Setup environment (install deps, start Kafka, create topics)"
    echo "2) Run Temperature Producer (Terminal 1)"
    echo "3) Run Temperature Processor (Terminal 2)"
    echo "4) Run Temperature Averages Consumer (Terminal 3)"
    echo "5) Run Temperature Alerts Consumer (Terminal 4)"
    echo "6) Run Manual Temperature Producer"
    echo "0) Exit"
    echo ""
    echo -n "Enter your choice [0-6]: "
    read choice

    case $choice in
        1)
            setup_environment
            ;;
        2)
            run_temperature_producer
            ;;
        3)
            run_temperature_processor
            ;;
        4)
            run_averages_consumer
            ;;
        5)
            run_alerts_consumer
            ;;
        6)
            run_manual_producer
            ;;
        0)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Press Enter to continue..."
            read
            show_menu
            ;;
    esac
}

# Make the script executable
chmod +x "$0"

# Main script logic - show the menu
show_menu 