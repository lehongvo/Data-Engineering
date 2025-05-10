#!/bin/bash

# Comprehensive script to set up and run the entire Kafka-Flink-BigQuery pipeline

# Remove version tag from docker-compose.yml if it exists
remove_version_tag() {
    # Check if file has version tag
    if grep -q "^version:" docker-compose.yml; then
        # Create temporary file without version tag
        grep -v "^version:" docker-compose.yml > docker-compose.yml.temp
        # Replace original file
        mv docker-compose.yml.temp docker-compose.yml
        echo "✓ Version tag removed from docker-compose.yml"
    fi
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Working directories
WORKING_DIR=$(pwd)
CONFIG_DIR="$WORKING_DIR/config"
CODE_DIR="$WORKING_DIR/code"
DATA_DIR="$WORKING_DIR/data"

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}===== Checking prerequisites =====${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
        exit 1
    fi
    
    # Check pip3
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}pip3 is not installed. Please install pip3 first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All prerequisites are met${NC}"
}

# Create necessary directories
create_directories() {
    echo -e "${BLUE}===== Creating directory structure =====${NC}"
    mkdir -p $DATA_DIR
    mkdir -p $CONFIG_DIR
    mkdir -p $DATA_DIR/results
    mkdir -p jars
    
    # Create log directories
    LOG_DIR="$DATA_DIR/logs"
    mkdir -p $LOG_DIR
    
    # Set permissions (ensure both local user and docker containers can write)
    chmod -R 777 $DATA_DIR/results
    chmod -R 777 $LOG_DIR
    
    # Create specific log files if they don't exist
    touch $LOG_DIR/kafka_producer.log
    touch $LOG_DIR/flink_processor.log
    
    # Set permissions on log files
    chmod 666 $LOG_DIR/*.log
    
    echo -e "${GREEN}✓ Created necessary directories${NC}"
    echo -e "${YELLOW}Log files:${NC}"
    echo -e "${YELLOW}  - $LOG_DIR/kafka_producer.log${NC}"
    echo -e "${YELLOW}  - $LOG_DIR/flink_processor.log${NC}"
}

# Install Python dependencies
install_dependencies() {
    echo -e "${BLUE}===== Installing Python dependencies =====${NC}"
    pip3 install kafka-python apache-flink google-cloud-bigquery uuid
    echo -e "${GREEN}✓ Installed Python dependencies${NC}"
}

# Check Google Cloud account key
check_account_key() {
    if [ ! -f "$CONFIG_DIR/account_key.json" ]; then
        echo -e "${RED}account_key.json file not found in $CONFIG_DIR${NC}"
        echo -e "${YELLOW}Please make sure you create this file before connecting to BigQuery${NC}"
        echo -e "${YELLOW}You can create a service account key in Google Cloud Console:${NC}"
        echo -e "${YELLOW}1. Go to IAM & Admin > Service Accounts${NC}"
        echo -e "${YELLOW}2. Create a service account with BigQuery Admin permissions${NC}"
        echo -e "${YELLOW}3. Create and download a JSON key${NC}"
        echo -e "${YELLOW}4. Save it as $CONFIG_DIR/account_key.json${NC}"
        return 1
    else
        # Validate the key file contains valid JSON
        if ! jq -e . "$CONFIG_DIR/account_key.json" >/dev/null 2>&1; then
            echo -e "${RED}account_key.json file exists but is not valid JSON${NC}"
            echo -e "${YELLOW}Please check the file contents and format${NC}"
            return 1
        fi
        
        echo -e "${GREEN}✓ Account key exists and is valid JSON${NC}"
        return 0
    fi
}

# Download Flink connector JARs
download_connector_jars() {
    echo -e "${BLUE}===== Downloading Flink connector JARs =====${NC}"
    
    # Create the jars directory if it doesn't exist
    mkdir -p jars
    
    # URLs for the required JARs
    KAFKA_CONNECTOR_URL="https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka_2.12/1.16.1/flink-connector-kafka_2.12-1.16.1.jar"
    KAFKA_CLIENT_URL="https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.1/kafka-clients-2.8.1.jar"
    FLINK_JSON_URL="https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.16.1/flink-json-1.16.1.jar"
    FLINK_CONNECTOR_BASE_URL="https://repo1.maven.org/maven2/org/apache/flink/flink-connector-base/1.16.1/flink-connector-base-1.16.1.jar"
    
    # Download the JARs if they don't exist
    if [ ! -f "jars/flink-connector-kafka_2.12-1.16.1.jar" ]; then
        echo -e "${YELLOW}Downloading Kafka connector...${NC}"
        curl -s -o jars/flink-connector-kafka_2.12-1.16.1.jar $KAFKA_CONNECTOR_URL
    fi
    
    if [ ! -f "jars/kafka-clients-2.8.1.jar" ]; then
        echo -e "${YELLOW}Downloading Kafka client...${NC}"
        curl -s -o jars/kafka-clients-2.8.1.jar $KAFKA_CLIENT_URL
    fi
    
    if [ ! -f "jars/flink-json-1.16.1.jar" ]; then
        echo -e "${YELLOW}Downloading Flink JSON...${NC}"
        curl -s -o jars/flink-json-1.16.1.jar $FLINK_JSON_URL
    fi
    
    if [ ! -f "jars/flink-connector-base-1.16.1.jar" ]; then
        echo -e "${YELLOW}Downloading Flink connector base...${NC}"
        curl -s -o jars/flink-connector-base-1.16.1.jar $FLINK_CONNECTOR_BASE_URL
    fi
    
    echo -e "${GREEN}✓ Downloaded required JARs${NC}"
}

# Start containers
start_containers() {
    echo -e "${BLUE}===== Starting containers =====${NC}"
    docker-compose down || true
    
    # Choose fastest build method based on environment
    if [ -n "$FAST_BUILD" ] && [ "$FAST_BUILD" = "parallel" ]; then
        echo -e "${YELLOW}Using parallel build for faster compilation...${NC}"
        docker-compose build --parallel
    elif [ -n "$FAST_BUILD" ] && [ "$FAST_BUILD" = "buildkit" ]; then
        echo -e "${YELLOW}Using BuildKit for faster compilation...${NC}"
        DOCKER_BUILDKIT=1 docker-compose build
    else
        # Default to standard build
        echo -e "${YELLOW}Using standard build (set FAST_BUILD=parallel or FAST_BUILD=buildkit for faster builds)${NC}"
        docker-compose build
    fi
    
    docker-compose up -d
    echo -e "${GREEN}✓ Started containers${NC}"
    
    echo -e "${YELLOW}Waiting for containers to fully start...${NC}"
    sleep 60
}

# Check Kafka
check_kafka() {
    echo -e "${BLUE}===== Checking Kafka =====${NC}"
    kafka_ready=$(docker exec e1-kafka kafka-topics --list --bootstrap-server e1-kafka:9092 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo -e "${RED}Kafka is not ready. Please check the logs:${NC}"
        echo -e "${YELLOW}docker-compose logs e1-kafka${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Kafka is ready!${NC}"
        return 0
    fi
}

# Set up BigQuery
setup_bigquery() {
    echo -e "${BLUE}===== Setting up BigQuery =====${NC}"
    
    if ! check_account_key; then
        return 1
    fi
    
    # Check Google Cloud SDK
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}Google Cloud SDK is not installed. Please install it first.${NC}"
        return 1
    fi
    
    # Use information from existing account key
    PROJECT_ID="unique-axle-457602-n6"
    DATASET_ID="clickstream_analytics"
    TABLE_NAME="user_page_stats"
    
    # Set up project
    echo -e "${YELLOW}Setting up Google Cloud project: $PROJECT_ID${NC}"
    gcloud config set project $PROJECT_ID
    
    # Set up credentials
    echo -e "${YELLOW}Setting up credentials from existing account key${NC}"
    export GOOGLE_APPLICATION_CREDENTIALS="$CONFIG_DIR/account_key.json"
    
    # Create dataset if it doesn't exist
    echo -e "${YELLOW}Creating BigQuery Dataset $DATASET_ID${NC}"
    bq --location=US mk --dataset $PROJECT_ID:$DATASET_ID
    
    # Create table
    echo -e "${YELLOW}Creating BigQuery Table $TABLE_NAME${NC}"
    bq mk --table $PROJECT_ID:$DATASET_ID.$TABLE_NAME \
        user_id:STRING,page:STRING,view_count:INTEGER,avg_session_duration:FLOAT,last_activity:STRING
    
    echo -e "${GREEN}✓ BigQuery set up with existing account key:${NC}"
    echo -e "${GREEN}Project ID: $PROJECT_ID${NC}"
    echo -e "${GREEN}Dataset ID: $DATASET_ID${NC}"
    echo -e "${GREEN}Table name: $TABLE_NAME${NC}"
    
    return 0
}

# Prepare Flink job
prepare_flink_job() {
    echo -e "${BLUE}===== Preparing Flink job =====${NC}"
    
    # Create config directory in Flink container
    docker exec flink-jobmanager mkdir -p /opt/flink/config
    
    # Copy necessary files to container
    docker cp $CODE_DIR/consumer/flink_processor.py flink-jobmanager:/opt/flink/
    
    if [ -f "$CONFIG_DIR/account_key.json" ]; then
        docker cp $CONFIG_DIR/account_key.json flink-jobmanager:/opt/flink/config/
        echo -e "${GREEN}✓ Copied account key to Flink container${NC}"
        
        # Set permissions to ensure file is readable
        docker exec flink-jobmanager chmod 644 /opt/flink/config/account_key.json
        echo -e "${GREEN}✓ Set read permissions for account key in Flink container${NC}"
    else
        echo -e "${YELLOW}Account key not found, will not connect to BigQuery${NC}"
    fi
    
    echo -e "${GREEN}✓ Prepared Flink job${NC}"
}

# Start Flink job
start_flink_job() {
    echo -e "${BLUE}===== Starting Flink job =====${NC}"
    docker exec -d flink-jobmanager /bin/bash -c 'cd /opt/flink && python3 flink_processor.py'
    echo -e "${GREEN}✓ Started Flink job${NC}"
}

# Start Kafka producer
start_kafka_producer() {
    echo -e "${BLUE}===== Starting Kafka producer =====${NC}"
    LOG_FILE="$DATA_DIR/logs/kafka_producer.log"
    python3 $CODE_DIR/producer/click_stream_producer.py > /dev/null 2>&1 &
    PRODUCER_PID=$!
    echo -e "${GREEN}✓ Started Kafka producer (PID: $PRODUCER_PID)${NC}"
    echo -e "${GREEN}✓ Logs being written to: $LOG_FILE${NC}"
}

# Display monitoring information
display_monitoring_info() {
    echo -e "\n${BLUE}===== Pipeline started successfully! =====${NC}"
    echo -e "${GREEN}Flink Dashboard: http://localhost:8081${NC}"
    echo -e "${GREEN}Kafka Producer PID: $PRODUCER_PID${NC}"
    
    if [ -f "$CONFIG_DIR/account_key.json" ]; then
        echo -e "${GREEN}Data is being processed and stored in BigQuery Project: unique-axle-457602-n6${NC}"
    fi
    
    echo -e "${GREEN}Data is also being saved to $DATA_DIR/results/part-*.json files${NC}"
    
    echo -e "\n${YELLOW}To stop the pipeline:${NC} docker-compose down"
    echo -e "${YELLOW}To check logs:${NC}"
    echo -e "  - Kafka: docker-compose logs -f e1-kafka"
    echo -e "  - Flink: docker-compose logs -f flink-jobmanager"
    echo -e "  - Kafka Producer: tail -f $DATA_DIR/logs/kafka_producer.log"
    echo -e "  - Flink Processor: tail -f $DATA_DIR/logs/flink_processor.log"
    echo -e "\n${YELLOW}To monitor the system:${NC} python3 $CODE_DIR/monitor.py"
}

# Stop pipeline
stop_pipeline() {
    echo -e "${BLUE}===== Stopping pipeline =====${NC}"
    
    # Find and stop Kafka producer
    PRODUCER_PIDS=$(ps aux | grep "click_stream_producer.py" | grep -v grep | awk '{print $2}')
    
    if [ ! -z "$PRODUCER_PIDS" ]; then
        kill $PRODUCER_PIDS
        echo -e "${GREEN}✓ Stopped Kafka producer${NC}"
    fi
    
    # Stop containers
    docker-compose down
    echo -e "${GREEN}✓ Stopped all containers${NC}"
}

# Show status
show_status() {
    echo -e "${BLUE}===== Pipeline Status =====${NC}"
    
    # Check containers
    echo -e "${YELLOW}Container status:${NC}"
    docker-compose ps
    
    # Check Kafka producer
    PRODUCER_PIDS=$(ps aux | grep "click_stream_producer.py" | grep -v grep | awk '{print $2}')
    if [ ! -z "$PRODUCER_PIDS" ]; then
        echo -e "${GREEN}Kafka producer is running (PID: $PRODUCER_PIDS)${NC}"
    else
        echo -e "${RED}Kafka producer is not running${NC}"
    fi
    
    # Check Flink jobs
    echo -e "${YELLOW}Flink jobs:${NC}"
    docker exec flink-jobmanager /opt/flink/bin/flink list -a
    
    # Check results files
    echo -e "${YELLOW}Results files:${NC}"
    ls -la $DATA_DIR/results/
}

# Set up the entire pipeline
setup_pipeline() {
    check_prerequisites
    remove_version_tag
    create_directories
    
    echo -e "${BLUE}===== Setting up logging =====${NC}"
    echo -e "${GREEN}✓ Log setup complete. Logs will be available in $DATA_DIR/logs/${NC}"
    
    install_dependencies
    download_connector_jars
    start_containers
    
    if ! check_kafka; then
        echo -e "${RED}Cannot set up pipeline because Kafka is not ready${NC}"
        return 1
    fi
    
    check_account_key
    
    # Ask user if they want to set up BigQuery
    read -p "Do you want to set up BigQuery? (y/n): " setup_bq
    if [[ "$setup_bq" == "y" || "$setup_bq" == "Y" ]]; then
        setup_bigquery
    fi
    
    prepare_flink_job
    
    echo -e "${GREEN}===== Pipeline setup complete! =====${NC}"
    return 0
}

# Run the entire pipeline
run_pipeline() {
    # Check if containers are running, if not run setup_pipeline
    if ! docker ps | grep -q "e1-kafka"; then
        echo -e "${YELLOW}Containers not started, setting up...${NC}"
        setup_pipeline
    fi
    
    # Check if Kafka is ready
    if ! check_kafka; then
        echo -e "${YELLOW}Restarting containers...${NC}"
        docker-compose down
        start_containers
        
        if ! check_kafka; then
            echo -e "${RED}Cannot run pipeline because Kafka is not ready${NC}"
            return 1
        fi
    fi
    
    prepare_flink_job
    start_flink_job
    start_kafka_producer
    display_monitoring_info
}

# Display menu
show_menu() {
    echo -e "${BLUE}===== KAFKA-FLINK-BIGQUERY PIPELINE =====${NC}"
    echo -e "${YELLOW}1. Set up pipeline${NC}"
    echo -e "${YELLOW}2. Run pipeline${NC}"
    echo -e "${YELLOW}3. Stop pipeline${NC}"
    echo -e "${YELLOW}4. View status${NC}"
    echo -e "${YELLOW}5. Set up BigQuery${NC}"
    echo -e "${YELLOW}6. Monitor pipeline${NC}"
    echo -e "${YELLOW}0. Exit${NC}"
    echo -e "${BLUE}=======================================${NC}"
    read -p "Enter your choice: " choice
    
    case $choice in
        1) setup_pipeline ;;
        2) run_pipeline ;;
        3) stop_pipeline ;;
        4) show_status ;;
        5) setup_bigquery ;;
        6) python3 $CODE_DIR/monitor.py ;;
        0) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}" ;;
    esac
}

# Main function
main() {
    # If command line arguments are provided, execute corresponding command
    if [ $# -ge 1 ]; then
        case $1 in
            "setup") setup_pipeline ;;
            "start" | "run") run_pipeline ;;
            "stop") stop_pipeline ;;
            "status") show_status ;;
            "bigquery") setup_bigquery ;;
            "monitor") python3 $CODE_DIR/monitor.py ;;
            *) show_menu ;;
        esac
    else
        # No arguments, display menu
        show_menu
    fi
}

# Start the program
main "$@"
