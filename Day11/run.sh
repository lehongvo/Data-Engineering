#!/bin/bash

# Setup function to initialize the environment
setup_environment() {
    echo "Setting up Flink environment..."
    
    # Create directories if they don't exist
    mkdir -p data code
    
    # Check if containers are already running
    if docker ps | grep -q flink-jobmanager; then
        echo "Flink containers are already running. Stopping them first..."
        docker-compose down
    fi
    
    # Clean up any existing containers/images to start fresh
    echo "Cleaning up any existing Flink containers and images..."
    docker-compose down --rmi local
    
    # Build and start Flink containers
    echo "Building and starting Flink containers..."
    
    # Pull base image first to speed up
    echo "Pulling base Flink image..."
    docker pull flink:latest
    
    echo "Building custom Flink image with Python..."
    # Build with verbose output to see what's happening
    docker-compose build --no-cache
    
    # Check if build was successful
    if [ $? -ne 0 ]; then
        echo "ERROR: Docker image build failed. Please check the error messages above."
        echo "Press Enter to continue..."
        read
        show_menu
        return
    fi
    
    echo "Starting containers..."
    docker-compose up -d
    
    # Wait for Flink to be ready
    echo "Waiting for Flink to be ready..."
    
    # Instead of sleeping fixed time, check if services are ready
    for i in {1..30}; do
        if curl -s http://localhost:8081 > /dev/null; then
            echo "Flink JobManager is ready!"
            break
        fi
        echo -n "."
        sleep 1
        if [ $i -eq 30 ]; then
            echo "Timeout waiting for Flink to start."
            echo "Checking logs for errors:"
            docker-compose logs
        fi
    done
    
    # Check Flink status
    echo "Checking Flink containers status..."
    docker ps | grep flink
    
    # Verify Python is available in the container
    echo "Verifying Python installation in container..."
    docker exec flink-jobmanager python3 --version || {
        echo "ERROR: Python is not available in the container!"
        echo "Checking container logs:"
        docker-compose logs
        echo "Press Enter to continue..."
        read
    }
    
    # Verify PyFlink is installed
    echo "Verifying PyFlink installation..."
    docker exec flink-jobmanager pip3 list | grep flink || {
        echo "WARNING: PyFlink might not be installed correctly."
        echo "Installing PyFlink in container..."
        docker exec -u root flink-jobmanager pip3 install apache-flink==1.16.1 pandas
    }
    
    echo "Environment setup complete!"
    
    # Return to main menu after setup is complete
    sleep 2
    show_menu
}

# Run Flink WordCount
run_wordcount() {
    echo "Running Flink WordCount job..."
    
    # Check if containers are running
    if ! docker ps | grep -q flink-jobmanager; then
        echo "Flink containers are not running. Please setup the environment first."
        sleep 2
        show_menu
        return
    fi
    
    # Check if Python is installed
    if ! docker exec flink-jobmanager python3 --version &>/dev/null; then
        echo "Python is not installed in the container. Installing Python..."
        docker exec -u root flink-jobmanager apt-get update
        docker exec -u root flink-jobmanager apt-get install -y python3 python3-pip python3-dev
        
        if [ $? -ne 0 ]; then
            echo "Failed to install Python. Please try setting up the environment again."
            sleep 2
            show_menu
            return
        fi
    fi
    
    # Check if PyFlink is installed
    if ! docker exec flink-jobmanager pip3 list | grep -q flink; then
        echo "PyFlink is not installed. Installing PyFlink..."
        docker exec -u root flink-jobmanager pip3 install apache-flink==1.16.1 pandas
        
        if [ $? -ne 0 ]; then
            echo "Failed to install PyFlink. Please try setting up the environment again."
            sleep 2
            show_menu
            return
        fi
    fi
    
    # Make sure the output directory exists and is empty
    mkdir -p data/output
    rm -f data/output/* 2>/dev/null
    
    # Run the WordCount job
    echo "Executing WordCount job..."
    docker exec -it flink-jobmanager python3 /code/word_count.py
    
    echo "Job completed!"
    
    # Show top results
    echo "Top 10 word counts:"
    if [ -d "data/output" ] && [ "$(ls -A data/output 2>/dev/null)" ]; then
        cat data/output/* | sort -nr -k2 | head -10
    else
        echo "Output directory is empty or not found. Job may have failed."
        echo "Checking container logs for errors:"
        docker logs flink-jobmanager | tail -20
    fi
    
    echo ""
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Show Flink Dashboard
open_dashboard() {
    echo "Opening Flink Dashboard..."
    echo "Please visit http://localhost:8081 in your browser"
    
    # Check if dashboard is actually accessible
    if command -v curl &> /dev/null; then
        if curl -s --head http://localhost:8081 | grep "200 OK" > /dev/null; then
            echo "Dashboard is accessible!"
        else
            echo "WARNING: Dashboard might not be accessible. Check if Flink is running correctly."
            echo "Checking container logs:"
            docker-compose logs | tail -20
        fi
    fi
    
    echo ""
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# View Results
view_results() {
    echo "Viewing WordCount Results..."
    
    if [ ! -d "data/output" ] || [ ! "$(ls -A data/output 2>/dev/null)" ]; then
        echo "Output directory is empty or not found. Please run the WordCount job first."
        sleep 2
        show_menu
        return
    fi
    
    echo "All words (sorted by count):"
    cat data/output/* | sort -nr -k2
    
    echo ""
    echo "Press Enter to return to the menu..."
    read
    
    show_menu
}

# Display menu and get user input
show_menu() {
    clear
    echo "========================================"
    echo "      APACHE FLINK WORDCOUNT - E1      "
    echo "========================================"
    echo "Please select an option:"
    echo ""
    echo "1) Setup environment (install deps, start Flink)"
    echo "2) Run WordCount job"
    echo "3) Open Flink Dashboard"
    echo "4) View WordCount results"
    echo "0) Exit"
    echo ""
    echo -n "Enter your choice [0-4]: "
    read choice

    case $choice in
        1)
            setup_environment
            ;;
        2)
            run_wordcount
            ;;
        3)
            open_dashboard
            ;;
        4)
            view_results
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