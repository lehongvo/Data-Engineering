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

    # Create input topic
    echo "Creating input-topic..."
    docker exec -it e1-kafka kafka-topics --create --topic input-topic --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 || echo "Topic may already exist"

    # Create output topic
    echo "Creating output-topic..."
    docker exec -it e1-kafka kafka-topics --create --topic output-topic --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 || echo "Topic may already exist"

    # List topics to verify
    echo "Verifying topics..."
    docker exec -it e1-kafka kafka-topics --list --bootstrap-server kafka:9092

    # Setup logging information
    echo "Setting up logging..."
    mkdir -p log
    touch log/input.log log/output.log

    echo "Environment setup complete!"
    
    # Return to main menu after setup is complete
    sleep 2
    clear
    show_menu
}

# Run Kafka Streams application
run_streams_app() {
    echo "Starting Kafka Streams application..."
    python3 kafka_uppercase.py
}

# Run producer
run_producer() {
    echo "Starting Kafka producer on input-topic..."
    echo "Type your messages and press Enter to send them. Press Ctrl+C to exit."
    docker exec -it e1-kafka kafka-console-producer --broker-list localhost:9094 --topic input-topic | tee -a log/input.log
}

# Run consumer
run_consumer() {
    echo "Starting Kafka consumer for output-topic..."
    echo "Messages will be displayed here. Press Ctrl+C to exit."
    docker exec -it e1-kafka kafka-console-consumer --bootstrap-server localhost:9094 --topic output-topic --from-beginning | tee -a log/output.log
}

# Display menu and get user input
show_menu() {
    clear
    echo "========================================"
    echo "      KAFKA STREAMS DEMO - E1          "
    echo "========================================"
    echo "Please select an option:"
    echo ""
    echo "1) Setup environment (install deps, start Kafka, create topics)"
    echo "2) Run Kafka Streams application (Terminal 1)"
    echo "3) Run producer to send messages (Terminal 2)"
    echo "4) Run consumer to receive messages (Terminal 3)"
    echo "0) Exit"
    echo ""
    echo -n "Enter your choice [0-4]: "
    read choice

    case $choice in
        1)
            setup_environment
            ;;
        2)
            run_streams_app
            ;;
        3)
            run_producer
            ;;
        4)
            run_consumer
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

# Main script logic - show the menu
show_menu
