#!/bin/bash
set -e

# Function to display menu
show_menu() {
    echo "=== Kafka Avro Schema Test Menu ==="
    echo "1. Start Services (Kafka, Zookeeper, Schema Registry)"
    echo "2. Test V1 Schema Only"
    echo "3. Test V2 Schema Only"
    echo "4. Test Schema Evolution (V1 -> V2)"
    echo "5. Test Schema Compatibility"
    echo "6. Cleanup (Stop all services and environment)"
    echo "7. Test schema error (producer sends invalid schema)"
    echo "0. Exit"
    echo "================================"
    echo -n "Enter your choice (0-7): "
}

# Function to start services
start_services() {
    echo "[1/4] Starting Kafka, Zookeeper, and Schema Registry with docker-compose..."
    docker-compose up -d
    sleep 5  # Wait for services to be ready
}

# Function to setup Python environment
setup_python_env() {
    echo "[2/4] Setting up Python virtual environment..."
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Function to run tests
run_test() {
    local test_type=$1
    echo "[3/4] Running test: $test_type"
    
    case $test_type in
        "v1")
            echo "Testing V1 schema only..."
            python code/producer_avro.py --schema-version 1 &
            PRODUCER_PID=$!
            sleep 2
            python code/consumer_avro.py --schema-version 1 &
            CONSUMER_PID=$!
            ;;
        "v2")
            echo "Testing V2 schema only..."
            python code/producer_avro.py --schema-version 2 &
            PRODUCER_PID=$!
            sleep 2
            python code/consumer_avro.py --schema-version 2 &
            CONSUMER_PID=$!
            ;;
        "evolution")
            echo "Testing schema evolution (V1 -> V2)..."
            # First run V1
            python code/producer_avro.py --schema-version 1 &
            PRODUCER_PID=$!
            sleep 2
            python code/consumer_avro.py --schema-version 1 &
            CONSUMER_PID=$!
            wait $PRODUCER_PID
            kill $CONSUMER_PID || true
            sleep 2
            # Then run V2
            python code/producer_avro.py --schema-version 2 &
            PRODUCER_PID=$!
            sleep 2
            python code/consumer_avro.py --schema-version 2 &
            CONSUMER_PID=$!
            ;;
        "compatibility")
            echo "Testing schema compatibility..."
            # Run both versions simultaneously
            python code/producer_avro.py --schema-version 1 &
            PRODUCER_PID1=$!
            python code/producer_avro.py --schema-version 2 &
            PRODUCER_PID2=$!
            sleep 2
            python code/consumer_avro.py --schema-version all &
            CONSUMER_PID=$!
            wait $PRODUCER_PID1
            wait $PRODUCER_PID2
            ;;
    esac

    # Wait for producer to finish and let consumer run for a while
    wait $PRODUCER_PID || true
    echo "Letting consumer run for 10 seconds..."
    sleep 10
    kill $CONSUMER_PID || true
}

# Function to save logs
save_logs() {
    echo "[4/4] Saving Docker logs to log directory..."
    mkdir -p log
    docker-compose logs kafka > log/kafka.log
    docker-compose logs zookeeper > log/zookeeper.log
    docker-compose logs schema-registry > log/schema-registry.log
}

# Function to cleanup
cleanup() {
    echo "Cleaning up..."
    docker-compose down
    rm -rf .venv
    echo "Cleanup complete!"
}

# Main script logic
while true; do
    show_menu
    read choice

    case $choice in
        1)
            start_services
            ;;
        2)
            start_services
            setup_python_env
            run_test "v1"
            save_logs
            ;;
        3)
            start_services
            setup_python_env
            run_test "v2"
            save_logs
            ;;
        4)
            start_services
            setup_python_env
            run_test "evolution"
            save_logs
            ;;
        5)
            start_services
            setup_python_env
            run_test "compatibility"
            save_logs
            ;;
        6)
            cleanup
            ;;
        7)
            start_services
            setup_python_env
            echo "[Schema error test] Producer will send invalid schema data..."
            python code/producer_avro_invalid.py
            save_logs
            ;;
        0)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac

    echo -e "\nPress Enter to continue..."
    read
done
