#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Make the script directory the working directory
cd "$(dirname "$0")"

# Check if Docker is installed and running
check_docker() {
    print_step "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi

    print_message "Docker is installed and running."
    
    if ! command -v docker-compose &> /dev/null; then
        print_warning "docker-compose is not installed as a standalone command."
        print_warning "Using 'docker compose' command instead."
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi
}

# Create necessary directories
create_directories() {
    print_step "Creating necessary directories..."
    mkdir -p data/zookeeper/data data/zookeeper/log data/kafka/data data/postgres data/warehouse data/kestra/storage
    mkdir -p logs output
    mkdir -p screenshots
    print_message "Directories created."
}

# Start Docker services
start_services() {
    print_step "Starting Docker services..."
    $DOCKER_COMPOSE down
    $DOCKER_COMPOSE up -d
    
    # Wait for services to initialize
    print_message "Waiting for services to initialize (20 seconds)..."
    sleep 20
    
    # Check if services are running
    if $DOCKER_COMPOSE ps | grep -q "kafka"; then
        print_message "Kafka is running."
    else
        print_error "Kafka failed to start. Check docker-compose logs."
        exit 1
    fi
    
    if $DOCKER_COMPOSE ps | grep -q "kestra"; then
        print_message "Kestra is running."
    else
        print_warning "Kestra may not be running. Check docker-compose logs."
    fi
}

# Upload Kestra flows
upload_kestra_flows() {
    print_step "Uploading Kestra flows..."
    
    # Wait for Kestra to be fully initialized
    print_message "Waiting for Kestra to be fully initialized (5 seconds)..."
    sleep 5
    
    # Make script executable if it's not already
    chmod +x upload_flows.sh
    
    # Execute the upload script
    ./upload_flows.sh
    
    if [ $? -eq 0 ]; then
        print_message "Kestra flows uploaded successfully."
    else
        print_error "Failed to upload Kestra flows. Check logs for details."
    fi
}

# Create Kafka topic
create_kafka_topic() {
    print_step "Creating Kafka topic..."
    # Wait for Kafka to be fully initialized
    print_message "Waiting for Kafka to be fully initialized (10 seconds)..."
    sleep 10
    
    $DOCKER_COMPOSE exec -T kafka \
    kafka-topics --bootstrap-server localhost:9092 --create --if-not-exists \
    --topic stock-market-data --partitions 1 --replication-factor 1
    
    if [ $? -eq 0 ]; then
        print_message "Kafka topic 'stock-market-data' created successfully."
    else
        print_error "Failed to create Kafka topic. Check if Kafka is running."
        exit 1
    fi
}

# Run Kafka producer
run_producer() {
    print_step "Running Kafka producer..."
    cd src/kafka
    print_message "Starting producer to generate 100 stock market data points..."
    KAFKA_BOOTSTRAP_SERVERS=localhost:29092 python3 producer.py &
    PRODUCER_PID=$!
    print_message "Producer started with PID: $PRODUCER_PID"
    cd ../..
    
    # Give the producer time to generate some data
    sleep 10
}

# Run Kafka consumer
run_consumer() {
    print_step "Running Kafka consumer..."
    cd src/kafka
    print_message "Starting consumer to read stock market data..."
    KAFKA_BOOTSTRAP_SERVERS=localhost:29092 python3 consumer.py &
    CONSUMER_PID=$!
    print_message "Consumer started with PID: $CONSUMER_PID"
    cd ../..
    
    # Give the consumer time to process data
    sleep 30
    
    # Stop the consumer
    kill $CONSUMER_PID
    print_message "Consumer stopped."
}

# Run Spark processing
run_spark_job() {
    print_step "Running Spark processing job..."
    cd src/spark
    print_message "Starting Spark job to process stock market data..."
    WAREHOUSE_JDBC_URL=jdbc:postgresql://localhost:5433/datawarehouse \
    WAREHOUSE_USER=datauser \
    WAREHOUSE_PASSWORD=datapass \
    python3 stock_processor.py
    cd ../..
}

# Create screenshots of the UI components
take_screenshots() {
    print_step "You should manually take screenshots of the following:"
    print_message "1. Kestra UI: http://localhost:8090"
    print_message "2. Kafka UI: http://localhost:8080"
    print_message "3. Data warehouse query results"
    print_message "Save these screenshots to the 'screenshots' directory."
}

# Check data warehouse
check_data_warehouse() {
    print_step "Checking data in the data warehouse..."
    print_message "Tables in the data warehouse:"
    $DOCKER_COMPOSE exec -T data-warehouse \
    psql -U datauser -d datawarehouse -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
    
    print_message "Sample data from stock_daily_stats:"
    $DOCKER_COMPOSE exec -T data-warehouse \
    psql -U datauser -d datawarehouse -c "SELECT * FROM stock_daily_stats LIMIT 5;"
}

# Install Python packages
install_python_packages() {
    print_step "Installing Python packages..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_message "Python packages installed successfully."
    else
        print_error "Failed to install Python packages."
        exit 1
    fi
}

# Stop all services
stop_services() {
    print_step "Stopping all services..."
    $DOCKER_COMPOSE down
    print_message "All services stopped."
}

# View logs
view_logs() {
    print_step "Available logs:"
    ls -la logs/
    
    echo
    echo "Enter log filename to view (or press Enter to go back):"
    read log_file
    
    if [ ! -z "$log_file" ]; then
        if [ -f "logs/$log_file" ]; then
            cat "logs/$log_file"
        else
            print_error "Log file not found: logs/$log_file"
        fi
    fi
}

# Run all steps
run_all() {
    check_docker
    create_directories
    start_services
    upload_kestra_flows
    create_kafka_topic
    run_producer
    run_consumer
    run_spark_job
    check_data_warehouse
    take_screenshots
}

# Main menu
show_menu() {
    clear
    echo "===== Stock Market Data Pipeline ====="
    echo
    echo "Choose an option:"
    echo
    echo "1) Start all (Full Start)"
    echo "2) Install Python packages"
    echo "3) Create directories and start services"
    echo "4) Upload Kestra flows"
    echo "5) Create Kafka topics"
    echo "6) Run Stock Market Producer"
    echo "7) Run Stock Market Consumer"
    echo "8) Run Spark Processing Job"
    echo "9) Check Data Warehouse"
    echo "10) Stop all services"
    echo "11) View logs"
    echo "0) Exit"
    echo
    echo -n "Enter your choice: "
    read choice
    
    case $choice in
        1)
            run_all
            ;;
        2)
            install_python_packages
            ;;
        3)
            check_docker
            create_directories
            start_services
            ;;
        4)
            upload_kestra_flows
            ;;
        5)
            create_kafka_topic
            ;;
        6)
            run_producer
            ;;
        7)
            run_consumer
            ;;
        8)
            run_spark_job
            ;;
        9)
            check_data_warehouse
            ;;
        10)
            stop_services
            ;;
        11)
            view_logs
            ;;
        0)
            echo "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option. Please try again."
            ;;
    esac
    
    echo
    echo "Press Enter to continue..."
    read
    show_menu
}

# Start the menu
check_docker
show_menu 