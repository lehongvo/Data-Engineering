#!/bin/bash

# Setup function to initialize the environment
setup_environment() {
    echo "Setting up Flink environment..."
    
    # Create directories if they don't exist
    mkdir -p data code
    
    # Stop existing containers and start new ones
    echo "Starting Flink containers..."
    docker-compose down
    docker-compose up -d
    
    # Wait for Flink to be ready
    echo "Waiting for Flink to be ready..."
    
    # Check if services are ready
    for i in {1..20}; do
        if curl -s http://localhost:8081/config > /dev/null 2>&1; then
            echo "Flink JobManager is ready!"
            break
        fi
        echo -n "."
        sleep 2
        if [ $i -eq 20 ]; then
            echo "Timeout waiting for Flink to start."
            echo "Checking logs for errors:"
            docker-compose logs
        fi
    done
    
    # Check Flink status
    echo "Checking Flink containers status..."
    docker ps | grep flink
    
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
        echo "Flink containers are not running. Please set up the environment first (option 4)."
        echo "Press Enter to return to the menu..."
        read
        show_menu
        return
    fi
    
    # Make sure the input directory exists with sample data
    if [ ! -f "data/input.txt" ]; then
        echo "Creating sample input data..."
        echo "Hello Apache Flink. Apache Flink is a framework and distributed processing engine for stateful computations over unbounded and bounded data streams." > data/input.txt
    fi
    
    # Force remove existing output directories on the container
    echo "Cleaning up previous output directories..."
    docker exec -it flink-jobmanager bash -c "rm -rf /data/output*"
    
    # Check if directories were successfully removed
    echo "Verifying cleanup..."
    docker exec -it flink-jobmanager ls -la /data
    
    # Run the WordCount job on a new file
    echo "Executing Flink WordCount job..."
    
    # Use the built-in examples from Flink
    docker exec -it flink-jobmanager bash -c "
        # Create a random output dir to avoid conflicts
        OUTPUT_DIR=/data/output_\$(date +%s)
        mkdir -p \$OUTPUT_DIR
        
        # Run the Flink WordCount example with properly specified class
        /opt/flink/bin/flink run \
            -c org.apache.flink.examples.java.wordcount.WordCount \
            /opt/flink/examples/batch/WordCount.jar \
            --input /data/input.txt \
            --output \$OUTPUT_DIR/result
        
        # Copy the results to the standard output directory
        mkdir -p /data/output
        cp -r \$OUTPUT_DIR/* /data/output/
    "
    
    echo "Job completed!"
    
    # Show top results
    echo "Top 10 word counts:"
    if [ -d "data/output" ] && [ "$(ls -A data/output 2>/dev/null)" ]; then
        cat data/output/* | head -10
    else
        echo "Output directory is empty or not found. Job may have failed."
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
    echo "      APACHE FLINK WORDCOUNT - E1      "
    echo "========================================"
    echo "Please select an option:"
    echo ""
    echo "1) Run WordCount job"
    echo "2) Open Flink Dashboard"
    echo "3) View WordCount results"
    echo "4) Setup Flink Environment"
    echo "5) Clean & Remove All Containers"
    echo "0) Exit"
    echo ""
    echo -n "Enter your choice [0-5]: "
    read choice

    case $choice in
        1)
            run_wordcount
            ;;
        2)
            open_dashboard
            ;;
        3)
            view_results
            ;;
        4)
            setup_environment
            ;;
        5)
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
setup_environment
# Main script logic - show menu
show_menu 