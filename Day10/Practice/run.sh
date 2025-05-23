#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[ETH-KAFKA]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Set the Practice directory path
PRACTICE_DIR="Practice"

# Debug - print Python path
print_step "Checking Python installation..."
echo "Python path: $(which python3)"
echo "Using explicit path: /usr/bin/python3"

# Check if Python and pip are installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi

    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        print_error "pip is not installed. Please install pip first."
        exit 1
    fi
}

# Install required dependencies
install_dependencies() {
    print_step "Installing required Python packages..."
    
    # Determine the correct path to requirements.txt
    local req_file
    if [ -f "requirements.txt" ]; then
        req_file="requirements.txt"
    elif [ -f "${PRACTICE_DIR}/requirements.txt" ]; then
        req_file="${PRACTICE_DIR}/requirements.txt"
    else
        print_error "requirements.txt not found."
        exit 1
    fi
    
    # Use pip3 if available, otherwise use pip
    if command -v pip3 &> /dev/null; then
        pip3 install -r "$req_file"
    else
        pip install -r "$req_file"
    fi
    
    if [ $? -eq 0 ]; then
        print_message "Packages installed successfully!"
    else
        print_error "Error installing packages. Please check the errors above."
        exit 1
    fi
}

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_warning "docker-compose is not installed. Please install docker-compose first."
        exit 1
    fi
}

# Create a .env file if it doesn't exist
create_env_file() {
    if [ ! -f "${PRACTICE_DIR}/.env" ]; then
        print_step "Creating .env file..."
        cat > "${PRACTICE_DIR}/.env" << EOL
# Ethereum provider API keys (not needed with the default public RPC endpoint)
# INFURA_KEY=
# ALCHEMY_KEY=

# Direct provider URL - Using LlamaRPC public endpoint
ETH_PROVIDER_URL=https://eth.llamarpc.com

# Kafka configuration (should match docker-compose.yml)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
EOL
        print_message ".env file created with default Ethereum RPC endpoint (https://eth.llamarpc.com)."
    fi
}

# Start Kafka and Zookeeper using Docker Compose
start_kafka() {
    print_step "Starting Kafka and Zookeeper..."
    # Check if we're already in the Practice directory
    if [ -f "docker-compose.yml" ]; then
        docker-compose down > /dev/null 2>&1  # Clean up any existing containers
        docker-compose up -d
    elif [ -f "${PRACTICE_DIR}/docker-compose.yml" ]; then
        (cd "${PRACTICE_DIR}" && docker-compose down > /dev/null 2>&1)  # Clean up any existing containers
        (cd "${PRACTICE_DIR}" && docker-compose up -d)
    else
        print_error "docker-compose.yml not found"
        return 1
    fi
    
    # Wait for Kafka to initialize
    print_message "Waiting for Kafka to start (15 seconds)..."
    sleep 15
}

# Stop Kafka and Zookeeper
stop_kafka() {
    print_step "Stopping Kafka and Zookeeper..."
    # Check if we're already in the Practice directory
    if [ -f "docker-compose.yml" ]; then
        docker-compose down
    elif [ -f "${PRACTICE_DIR}/docker-compose.yml" ]; then
        (cd "${PRACTICE_DIR}" && docker-compose down)
    else
        print_error "docker-compose.yml not found"
        return 1
    fi
}

# Create Kafka topics
create_topics() {
    print_step "Creating Kafka topics..."
    # Check if we're already in the Practice directory
    if [ -f "kafka_admin.py" ]; then
        python3 kafka_admin.py
    elif [ -f "${PRACTICE_DIR}/kafka_admin.py" ]; then
        (cd "${PRACTICE_DIR}" && python3 kafka_admin.py)
    else
        print_error "kafka_admin.py not found"
        return 1
    fi
}

# Run the producer
run_producer() {
    print_step "Starting Ethereum blockchain data producer..."
    # Check if we're already in the Practice directory
    if [ -f "eth_producer.py" ]; then
        python3 eth_producer.py
    elif [ -f "${PRACTICE_DIR}/eth_producer.py" ]; then
        (cd "${PRACTICE_DIR}" && python3 eth_producer.py)
    else
        print_error "eth_producer.py not found"
        return 1
    fi
}

# Run the consumer
run_consumer() {
    print_step "Starting Ethereum blockchain data consumer..."
    # Check if we're already in the Practice directory
    if [ -f "eth_consumer.py" ]; then
        python3 eth_consumer.py
    elif [ -f "${PRACTICE_DIR}/eth_consumer.py" ]; then
        (cd "${PRACTICE_DIR}" && python3 eth_consumer.py)
    else
        print_error "eth_consumer.py not found"
        return 1
    fi
}

# Run the streams processor
run_streams() {
    print_step "Starting Ethereum blockchain data stream processor..."
    # Check if we're already in the Practice directory
    if [ -f "eth_streams.py" ]; then
        python3 eth_streams.py
    elif [ -f "${PRACTICE_DIR}/eth_streams.py" ]; then
        (cd "${PRACTICE_DIR}" && python3 eth_streams.py)
    else
        print_error "eth_streams.py not found"
        return 1
    fi
}

# Run the Spark streams processor
run_spark() {
    print_step "Starting Spark streaming application for Ethereum data..."
    
    # Create output and checkpoint directories if they don't exist
    if [ -f "spark_streaming.py" ]; then
        mkdir -p output/address_volume output/contract_interactions output/gas_trends
        mkdir -p checkpoint/address_volume checkpoint/contract_interactions checkpoint/gas_trends
        python3 spark_streaming.py
    elif [ -f "${PRACTICE_DIR}/spark_streaming.py" ]; then
        (cd "${PRACTICE_DIR}" && mkdir -p output/address_volume output/contract_interactions output/gas_trends)
        (cd "${PRACTICE_DIR}" && mkdir -p checkpoint/address_volume checkpoint/contract_interactions checkpoint/gas_trends)
        (cd "${PRACTICE_DIR}" && python3 spark_streaming.py)
    else
        print_error "spark_streaming.py not found"
        return 1
    fi
}

# Run all components
run_all() {
    # Determine the correct path
    local script_path
    if [ -f "eth_producer.py" ]; then
        script_path="$(pwd)"
    elif [ -f "${PRACTICE_DIR}/eth_producer.py" ]; then
        script_path="$(pwd)/${PRACTICE_DIR}"
    else
        print_error "eth_producer.py not found"
        return 1
    fi

    # Start in separate terminal windows/tabs if possible
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e 'tell app "Terminal" to do script "cd '"${script_path}"' && python3 eth_producer.py"' &
        sleep 2
        osascript -e 'tell app "Terminal" to do script "cd '"${script_path}"' && python3 eth_consumer.py"' &
        sleep 2
        osascript -e 'tell app "Terminal" to do script "cd '"${script_path}"' && python3 eth_streams.py"' &
        sleep 2
        
        # Create directories needed for Spark
        mkdir -p "${script_path}/output/address_volume" "${script_path}/output/contract_interactions" "${script_path}/output/gas_trends"
        mkdir -p "${script_path}/checkpoint/address_volume" "${script_path}/checkpoint/contract_interactions" "${script_path}/checkpoint/gas_trends"
        
        # Start Spark streaming
        osascript -e 'tell app "Terminal" to do script "cd '"${script_path}"' && python3 spark_streaming.py"' &
    else
        # Linux/others - use screen or tmux if available
        if command -v tmux &> /dev/null; then
            tmux new-session -d -s eth-producer "cd ${script_path} && python3 eth_producer.py"
            tmux new-session -d -s eth-consumer "cd ${script_path} && python3 eth_consumer.py"
            tmux new-session -d -s eth-streams "cd ${script_path} && python3 eth_streams.py"
            
            # Create directories needed for Spark
            mkdir -p "${script_path}/output/address_volume" "${script_path}/output/contract_interactions" "${script_path}/output/gas_trends"
            mkdir -p "${script_path}/checkpoint/address_volume" "${script_path}/checkpoint/contract_interactions" "${script_path}/checkpoint/gas_trends"
            
            # Start Spark streaming
            tmux new-session -d -s spark-streams "cd ${script_path} && python3 spark_streaming.py"
            
            print_message "Started all components in tmux sessions. Use 'tmux attach -t <session-name>' to view."
        else
            # Just run in background with nohup
            if [ -f "eth_producer.py" ]; then
                # Create directories needed for Spark
                mkdir -p output/address_volume output/contract_interactions output/gas_trends
                mkdir -p checkpoint/address_volume checkpoint/contract_interactions checkpoint/gas_trends
                
                nohup python3 eth_producer.py > logs/producer.log 2>&1 &
                nohup python3 eth_consumer.py > logs/consumer.log 2>&1 &
                nohup python3 eth_streams.py > logs/streams.log 2>&1 &
                nohup python3 spark_streaming.py > logs/spark.log 2>&1 &
            elif [ -f "${PRACTICE_DIR}/eth_producer.py" ]; then
                # Create directories needed for Spark
                (cd "${PRACTICE_DIR}" && mkdir -p output/address_volume output/contract_interactions output/gas_trends)
                (cd "${PRACTICE_DIR}" && mkdir -p checkpoint/address_volume checkpoint/contract_interactions checkpoint/gas_trends)
                
                (cd "${PRACTICE_DIR}" && nohup python3 eth_producer.py > logs/producer.log 2>&1 &)
                (cd "${PRACTICE_DIR}" && nohup python3 eth_consumer.py > logs/consumer.log 2>&1 &)
                (cd "${PRACTICE_DIR}" && nohup python3 eth_streams.py > logs/streams.log 2>&1 &)
                (cd "${PRACTICE_DIR}" && nohup python3 spark_streaming.py > logs/spark.log 2>&1 &)
            fi
            print_message "Started all components in background. Check log files for output."
        fi
    fi
}

# Stop all running components
stop_all() {
    print_step "Stopping all components..."
    
    # Find and kill Python processes
    pkill -f "python3 eth_producer.py" 2>/dev/null
    pkill -f "python3 eth_consumer.py" 2>/dev/null
    pkill -f "python3 eth_streams.py" 2>/dev/null
    pkill -f "python3 spark_streaming.py" 2>/dev/null
    
    # Stop Docker containers
    # Check if we're already in the Practice directory
    if [ -f "docker-compose.yml" ]; then
        docker-compose down
    elif [ -f "${PRACTICE_DIR}/docker-compose.yml" ]; then
        (cd "${PRACTICE_DIR}" && docker-compose down)
    else
        print_error "docker-compose.yml not found"
        return 1
    fi
    
    print_message "All components stopped."
}

# Run with start-all command
run_start_all() {
    check_python
    install_dependencies
    check_docker
    create_env_file
    start_kafka
    create_topics
    run_all
    print_message "All components started!"
}

# View logs
view_logs() {
    print_step "Viewing log files..."
    
    # Check if we're already in the Practice directory
    if [ -d "logs" ]; then
        log_dir="logs"
    elif [ -d "${PRACTICE_DIR}/logs" ]; then
        log_dir="${PRACTICE_DIR}/logs"
    else
        print_error "Log directory not found"
        return 1
    fi
    
    # List available log files
    echo "Available log files:"
    ls -la "$log_dir"
    echo
    
    # Ask which log to view
    echo -n "Enter log file to view (e.g. eth-producer.log): "
    read -r log_file
    
    if [ -f "${log_dir}/${log_file}" ]; then
        # Use tail to view the log with follow option
        tail -f "${log_dir}/${log_file}"
    else
        print_error "Log file not found: ${log_file}"
    fi
}

# Show menu
show_menu() {
    clear
    echo "============================================"
    echo "   Ethereum Blockchain Data Processing with Kafka"
    echo "============================================"
    echo "Choose an option:"
    echo
    echo "1) Start all (Full Start)"
    echo "2) Install Python packages"
    echo "3) Run Kafka and Zookeeper"
    echo "4) Create Kafka topics"
    echo "5) Run Ethereum Producer"
    echo "6) Run Ethereum Consumer"
    echo "7) Run Ethereum Streams Processor"
    echo "8) Run Spark Streaming Application"
    echo "9) Stop all"
    echo "10) View logs"
    echo "0) Exit"
    echo
    echo -n "Enter your choice [0-10]: "
    read -r choice
    
    case $choice in
        1) run_start_all ;;
        2) check_python && install_dependencies ;;
        3) check_docker && start_kafka ;;
        4) create_topics ;;
        5) run_producer ;;
        6) run_consumer ;;
        7) run_streams ;;
        8) run_spark ;;
        9) stop_all ;;
        10) view_logs ;;
        0) exit 0 ;;
        *)
            print_error "Invalid choice!"
            sleep 2
            show_menu
            ;;
    esac
    
    if [ "$choice" != "0" ]; then
        echo
        echo -n "Press Enter to return to menu..."
        read -r dummy
        show_menu
    fi
}

# Main execution
show_menu 