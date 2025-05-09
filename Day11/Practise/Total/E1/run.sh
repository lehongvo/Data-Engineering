#!/bin/bash

# Setup function to initialize the environment
setup_environment() {
    echo "Setting up Kafka and Flink environment..."
    
    # Create directories if they don't exist
    mkdir -p data data/results
    
    # Stop existing containers and start new ones
    echo "Starting containers..."
    docker-compose down
    docker-compose up -d
    
    # Wait for Kafka and Flink to be ready
    echo "Waiting for services to be ready..."
    
    # Check if Flink JobManager is ready
    for i in {1..30}; do
        if curl -s http://localhost:8081/config > /dev/null 2>&1; then
            echo "Flink JobManager is ready!"
            break
        fi
        echo -n "."
        sleep 2
        if [ $i -eq 30 ]; then
            echo "Timeout waiting for Flink to start."
        fi
    done
    
    # Check if Kafka is ready
    for i in {1..10}; do
        if docker exec kafka kafka-topics --bootstrap-server=localhost:9092 --list 2>/dev/null; then
            echo "Kafka is ready!"
            break
        fi
        echo -n "."
        sleep 2
        if [ $i -eq 30 ]; then
            echo "Timeout waiting for Kafka to start."
        fi
    done
    
    # Install Python dependencies on the Python container
    echo "Installing Python dependencies..."
    docker exec python-tools pip install -r /code/requirements.txt
    
    # Create Kafka topics
    echo "Creating Kafka topics..."
    docker exec kafka kafka-topics --create --bootstrap-server=localhost:9092 --topic sales-data --partitions 4 --replication-factor 1 --if-not-exists
    docker exec kafka kafka-topics --create --bootstrap-server=localhost:9092 --topic hourly-revenue --partitions 4 --replication-factor 1 --if-not-exists
    
    echo "Environment setup complete!"
    
    # Return to main menu after setup is complete
    sleep 2
    show_menu
}

# Generate data for benchmarking
generate_data() {
    echo "Generating sales data for benchmarking..."
    
    # Default values
    COUNT=1000000
    
    # Ask for record count
    read -p "Enter number of records to generate (default: 1,000,000): " input_count
    if [ ! -z "$input_count" ]; then
        COUNT=$input_count
    fi
    
    echo "Generating $COUNT records..."
    docker exec -it python-tools python /code/generate_sales_data.py --count $COUNT --output /data/sales_data.json
    
    echo "Data generation complete!"
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Run full benchmark comparison
run_benchmark() {
    echo "Running benchmark comparison between Apache Flink and Kafka..."
    
    # Check if containers are running
    if ! docker ps | grep -q flink-jobmanager; then
        echo "Containers are not running. Please set up the environment first (option 3)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Check if the data file exists
    if [ ! -f "data/sales_data.json" ]; then
        echo "Sales data file not found. Please generate data first (option 1)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Run benchmark
    echo "Starting benchmark..."
    docker exec -it python-tools python /code/run_benchmark.py --data-path /data/sales_data.json --output-dir /data/results
    
    echo "Benchmark complete! Check results in data/results directory."
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Run only the Flink implementation
run_flink() {
    echo "Running Apache Flink sales analysis..."
    
    # Check if containers are running
    if ! docker ps | grep -q flink-jobmanager; then
        echo "Containers are not running. Please set up the environment first (option 3)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Check if the data file exists
    if [ ! -f "data/sales_data.json" ]; then
        echo "Sales data file not found. Please generate data first (option 1)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Get parallelism
    read -p "Enter parallelism level (default: 1): " parallelism
    if [ -z "$parallelism" ]; then
        parallelism=1
    fi
    
    # Create output directory
    mkdir -p data/results/flink_only
    
    # Run Flink analysis
    echo "Starting Flink analysis..."
    docker exec -it python-tools python /code/flink/sales_analysis.py --input /data/sales_data.json --output /data/results/flink_only --parallelism $parallelism
    
    echo "Flink analysis complete! Check results in data/results/flink_only directory."
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Run only the Kafka implementation
run_kafka() {
    echo "Running Kafka sales analysis..."
    
    # Check if containers are running
    if ! docker ps | grep -q kafka; then
        echo "Containers are not running. Please set up the environment first (option 3)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Check if the data file exists
    if [ ! -f "data/sales_data.json" ]; then
        echo "Sales data file not found. Please generate data first (option 1)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Create output directory
    mkdir -p data/results/kafka_only
    
    # Run Kafka analysis
    echo "Starting Kafka analysis..."
    docker exec -it python-tools python /code/kafka/sales_analysis.py --input /data/sales_data.json --output /data/results/kafka_only
    
    echo "Kafka analysis complete! Check results in data/results/kafka_only directory."
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# View Flink dashboard
open_flink_dashboard() {
    echo "Opening Flink Dashboard..."
    echo "Please visit http://localhost:8081 in your browser"
    
    # Check if dashboard is actually accessible
    if command -v curl &> /dev/null; then
        if curl -s --head http://localhost:8081 | grep "200 OK" > /dev/null; then
            echo "Dashboard is accessible!"
        else
            echo "WARNING: Dashboard might not be accessible. Check if Flink is running correctly."
        fi
    fi
    
    echo ""
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Clean all containers and rebuild
clean_rebuild() {
    echo "Cleaning all containers and rebuilding..."
    
    # Stop and remove all containers
    docker-compose down --rmi all
    
    # Clean up Docker cache
    docker system prune -f
    
    echo "Cleanup complete!"
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Display menu and get user input
show_menu() {
    clear
    echo "========================================================"
    echo "      APACHE FLINK VS KAFKA STREAMS BENCHMARK"
    echo "========================================================"
    echo "Please select an option:"
    echo ""
    echo "1) Generate Sales Data"
    echo "2) Run Full Benchmark Comparison"
    echo "3) Setup Environment"
    echo "4) Run Flink Analysis Only"
    echo "5) Run Kafka Analysis Only"
    echo "6) Open Flink Dashboard"
    echo "7) Clean & Remove All Containers"
    echo "0) Exit"
    echo ""
    echo -n "Enter your choice [0-7]: "
    read choice

    case $choice in
        1)
            generate_data
            ;;
        2)
            run_benchmark
            ;;
        3)
            setup_environment
            ;;
        4)
            run_flink
            ;;
        5)
            run_kafka
            ;;
        6)
            open_flink_dashboard
            ;;
        7)
            clean_rebuild
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

# Main script logic - show menu
show_menu 