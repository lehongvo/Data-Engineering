#!/bin/bash

# Setup function to initialize the environment
setup_environment() {
    echo "Setting up Flink environment..."
    
    # Create directories if they don't exist
    mkdir -p data
    mkdir -p code
    
    # Check for required files
    if [ ! -f "code/requirements.txt" ] || [ ! -f "code/web_log_analysis.py" ] || [ ! -f "code/generate_logs.py" ]; then
        echo "Required files missing in code directory. Checking..."
        if [ ! -d "code" ]; then
            echo "Code directory doesn't exist. Creating it..."
            mkdir -p code
        fi
    fi
    
    # Stop existing containers and start new ones
    echo "Starting Flink containers..."
    docker-compose down
    docker-compose up -d
    
    # Wait for Flink to be ready
    echo "Waiting for Flink to be ready..."
    
    # Check if services are ready
    for i in {1..30}; do
        if curl -s http://localhost:8082/config > /dev/null 2>&1; then
            echo "Flink JobManager is ready!"
            break
        fi
        echo -n "."
        sleep 2
        if [ $i -eq 30 ]; then
            echo "Timeout waiting for Flink to start."
            echo "Checking logs for errors:"
            docker-compose logs
        fi
    done
    
    # Check if all containers are running
    echo "Verifying all containers are running..."
    
    # Check Python container
    if ! docker ps | grep -q python-e2; then
        echo "Python container is not running. Starting it..."
        docker-compose up -d python
        sleep 5
    fi
    
    # Create a marker file to track if we've already installed Python
    MARKER_FILE="data/.python_installed"
    
    # Check if Python is already installed by looking for our marker file
    if [ ! -f "$MARKER_FILE" ]; then
        # Install Python and dependencies in the Flink JobManager container
        echo "Installing Python in Flink JobManager container..."
        docker exec flink-jobmanager-e2 bash -c "apt-get update && apt-get install -y python3 python3-pip && ln -sf /usr/bin/python3 /usr/bin/python && pip3 install apache-flink==1.16.1 pandas python-dateutil py4j numpy"
        
        # Create marker file to avoid reinstalling
        touch "$MARKER_FILE"
        echo "Python installation complete."
    else
        echo "Python is already installed in Flink JobManager container."
    fi
    
    # Check Flink status
    echo "Checking Flink containers status..."
    docker ps | grep flink
    
    echo "Environment setup complete!"
    
    # Return to main menu after setup is complete
    sleep 2
    show_menu
}

# Generate log data
generate_logs() {
    echo "Generating web access logs..."
    
    # Check if containers are running
    if ! docker ps | grep -q python-e2; then
        echo "Python container is not running. Setting up environment first..."
        setup_environment
    fi
    
    docker exec python-e2 python generate_logs.py --count 5000 --output /data/web_logs.json
    
    echo "Logs generated successfully!"
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Run Flink Web Log Analysis
run_web_log_analysis() {
    echo "Running Flink Web Log Analysis job..."
    
    # Check if containers are running
    if ! docker ps | grep -q flink-jobmanager-e2; then
        echo "Flink containers are not running. Setting up environment first..."
        setup_environment
    else
        # Ensure Python is installed before running the job
        echo "Checking Python installation..."
        MARKER_FILE="data/.python_installed"
        if [ ! -f "$MARKER_FILE" ]; then
            echo "Python not detected. Setting up environment first..."
            setup_environment
        fi
    fi
    
    # Check if the logs file exists
    if [ ! -f "data/web_logs.json" ]; then
        echo "Log file not found. Please generate logs first (option 1)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Clean previous output
    echo "Cleaning up previous output directories..."
    rm -rf data/output
    mkdir -p data/output
    
    # Run the web log analysis job
    echo "Executing Flink Web Log Analysis job..."
    docker exec flink-jobmanager-e2 bash -c "cd /code && /opt/flink/bin/flink run -py /code/web_log_analysis.py --pyFiles /code/web_log_analysis.py"
    
    echo "Job executed. Check results in data/output directory."
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Show Flink Dashboard
open_dashboard() {
    echo "Opening Flink Dashboard..."
    echo "Please visit http://localhost:8082 in your browser"
    
    # Check if dashboard is actually accessible
    if command -v curl &> /dev/null; then
        if curl -s --head http://localhost:8082 | grep "200 OK" > /dev/null; then
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

# View Results
view_results() {
    echo "Viewing Analysis Results..."
    
    # Check if results exist
    if [ ! -d "data/output" ] || [ -z "$(ls -A data/output 2>/dev/null)" ]; then
        echo "Output directory is empty or not found. Please run the analysis job first."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    echo "=== ERROR REQUESTS ==="
    if [ -d "data/output/error_requests" ] && [ -n "$(ls -A data/output/error_requests 2>/dev/null)" ]; then
        head -20 data/output/error_requests/*
    else
        echo "No error requests found."
    fi
    
    echo ""
    echo "=== URL COUNTS (10-minute windows) ==="
    if [ -d "data/output/url_counts" ] && [ -n "$(ls -A data/output/url_counts 2>/dev/null)" ]; then
        head -20 data/output/url_counts/*
    else
        echo "No URL counts found."
    fi
    
    echo ""
    echo "=== ABNORMAL IPs (with excessive error requests) ==="
    if [ -d "data/output/abnormal_ips" ] && [ -n "$(ls -A data/output/abnormal_ips 2>/dev/null)" ]; then
        cat data/output/abnormal_ips/*
    else
        echo "No abnormal IPs found."
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
    echo "========================================"
    echo "      APACHE FLINK WEB LOG ANALYSIS    "
    echo "========================================"
    echo "Please select an option:"
    echo ""
    echo "1) Generate Web Access Logs"
    echo "2) Run Web Log Analysis job"
    echo "3) Setup Flink Environment"
    echo "4) Open Flink Dashboard"
    echo "5) View Analysis Results"
    echo "6) Clean & Remove All Containers"
    echo "0) Exit"
    echo ""
    echo -n "Enter your choice [0-6]: "
    read choice

    case $choice in
        1)
            generate_logs
            ;;
        2)
            run_web_log_analysis
            ;;
        3)
            setup_environment
            ;;
        4)
            open_dashboard
            ;;
        5)
            view_results
            ;;
        6)
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
setup_environment 