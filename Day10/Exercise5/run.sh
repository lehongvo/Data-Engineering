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

# Determine pip command (pip or pip3)
determine_pip_command() {
    if command -v pip3 &> /dev/null; then
        echo "pip3"
    elif command -v pip &> /dev/null; then
        echo "pip"
    else
        echo ""
    fi
}

# Check Python and required packages
check_requirements() {
    print_step "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi

    print_message "Python is installed."
    
    # Determine pip command
    PIP_CMD=$(determine_pip_command)
    
    if [ -z "$PIP_CMD" ]; then
        print_error "Neither pip nor pip3 found. Please install pip for Python 3."
        exit 1
    fi
    
    print_message "Using $PIP_CMD for package installation."
    
    # Always install required packages to ensure all dependencies are available
    print_step "Installing required Python packages..."
    $PIP_CMD install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        print_error "Failed to install required Python packages."
        exit 1
    fi
    
    # Explicitly ensure google-cloud-bigquery and other critical packages are installed
    print_step "Verifying critical packages..."
    $PIP_CMD install google-cloud-bigquery pandas-gbq pyarrow db-dtypes
    
    if [ $? -ne 0 ]; then
        print_error "Failed to install critical packages."
        exit 1
    fi
    
    print_message "All required packages installed."
}

# Create necessary directories
create_directories() {
    print_step "Creating necessary directories..."
    mkdir -p data logs output/{charts,reports} screenshots config
    print_message "Directories created."
}

# Setup Spark BigQuery connector
setup_spark_bigquery() {
    print_step "Setting up Spark BigQuery connector..."
    
    # Create jars directory if it doesn't exist
    mkdir -p jars
    
    # Download connector if it doesn't exist
    CONNECTOR_JAR="jars/spark-bigquery-connector.jar"
    if [ ! -f "$CONNECTOR_JAR" ]; then
        print_message "Downloading Spark BigQuery connector..."
        if command -v curl &> /dev/null; then
            curl -L "https://storage.googleapis.com/spark-lib/bigquery/spark-bigquery-latest_2.12.jar" -o "$CONNECTOR_JAR"
        elif command -v wget &> /dev/null; then
            wget "https://storage.googleapis.com/spark-lib/bigquery/spark-bigquery-latest_2.12.jar" -O "$CONNECTOR_JAR"
        else
            print_error "Neither curl nor wget found. Cannot download connector."
            return 1
        fi
        
        if [ $? -ne 0 ]; then
            print_error "Failed to download Spark BigQuery connector."
            return 1
        fi
    fi
    
    # Ensure service account key directory
    if [ ! -d "config" ]; then
        mkdir -p config
        print_warning "Created config directory. Please place your service account key in config/account_key.json"
    fi
    
    # Set connector path environment variable
    export SPARK_CONNECTOR_PATH="$(pwd)/$CONNECTOR_JAR"
    export SPARK_JARS="$(pwd)/$CONNECTOR_JAR"
    
    print_message "Spark BigQuery connector setup completed."
    return 0
}

# Extract project ID from service account key
extract_project_id() {
    # This function extracts the project_id from the service account key
    if [ -f "config/account_key.json" ]; then
        cat config/account_key.json | grep project_id | head -1 | awk -F'"' '{print $4}'
    else
        print_error "Service account key file not found at config/account_key.json"
        print_warning "Using sample project ID for demonstration"
        echo "unique-axle-457602-n6"
    fi
}

# Run BigQuery data extraction and Spark analysis
run_integration() {
    print_step "Running BigQuery-Spark integration..."
    
    # Setup Spark BigQuery connector
    setup_spark_bigquery
    if [ $? -ne 0 ]; then
        print_error "Failed to setup Spark BigQuery connector. Exiting."
        exit 1
    fi
    
    # Get GCP project ID
    print_step "Extracting GCP project ID from service account key..."
    PROJECT_ID=$(extract_project_id)
    
    if [ -z "$PROJECT_ID" ]; then
        print_error "Could not extract project ID from service account key."
        exit 1
    fi
    
    print_message "Using GCP project ID: $PROJECT_ID"
    
    # Example datasets to analyze
    print_message "Available public datasets in BigQuery:"
    echo "1. bigquery-public-data.samples.natality (Birth data)"
    echo "2. bigquery-public-data.austin_311.311_service_requests (City service requests)"
    echo "3. bigquery-public-data.samples.gsod (Global weather data)"
    
    read -p "Enter the dataset number to analyze (1-3) or press Enter for default: " DATASET_CHOICE
    
    case $DATASET_CHOICE in
        1)
            DATASET="bigquery-public-data.samples.natality"
            QUERY_LIMIT=5000
            print_message "Selected: Birth data"
            ;;
        2)
            DATASET="bigquery-public-data.austin_311.311_service_requests"
            QUERY_LIMIT=5000
            print_message "Selected: City service requests"
            ;;
        3)
            DATASET="bigquery-public-data.samples.gsod"
            QUERY_LIMIT=5000
            print_message "Selected: Global weather data"
            ;;
        *)
            DATASET="bigquery-public-data.samples.natality"
            QUERY_LIMIT=2000
            print_message "Using default: Birth data"
            ;;
    esac
    
    # Export environment variables for Spark
    export PYTHONPATH="$(pwd):$PYTHONPATH"
    export PYSPARK_PYTHON=python3
    export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/config/account_key.json"
    
    # Set Spark configuration for BigQuery connector
    CONNECTOR_JAR="$(pwd)/jars/spark-bigquery-connector.jar"
    export SPARK_CONNECTOR_PATH="$CONNECTOR_JAR"
    export PYSPARK_SUBMIT_ARGS="--jars $CONNECTOR_JAR pyspark-shell"
    
    print_message "Using Spark BigQuery connector: $CONNECTOR_JAR"
    
    # Extract data from BigQuery and analyze with PySpark
    print_message "Extracting data from $DATASET and processing with Spark..."
    python3 -c "
import os
import sys
sys.path.append('src')
from bigquery_spark_integration import BigQuerySparkIntegration
from data_analysis import *
from reporting import SparkReporting

os.makedirs('logs', exist_ok=True)

try:
    # Initialize the integration
    integration = BigQuerySparkIntegration(
        project_id='$PROJECT_ID',
        credentials_path='config/account_key.json'
    )
    
    # Extract data from BigQuery
    query = f'(SELECT * FROM \`$DATASET\` LIMIT $QUERY_LIMIT)'
    df = integration.extract_from_bigquery(query, 'data')
    
    # Get column names for analysis
    columns = df.columns
    
    # Find numeric columns for analysis
    numeric_cols = [f.name for f in df.schema.fields 
                   if f.dataType.typeName() in ['double', 'integer', 'long', 'float']]
    
    # Find categorical columns
    categorical_cols = [f.name for f in df.schema.fields
                      if f.dataType.typeName() in ['string']]
    
    # Sample analyses
    print('Performing analyses...')
    
    # 1. Calculate statistics by segment
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        segment_col = categorical_cols[0]
        value_col = numeric_cols[0]
        segment_analysis = segment_and_analyze(df, segment_col, value_col)
        
        # Write results to BigQuery
        integration.write_to_bigquery(segment_analysis, 'analysis_results.segment_analysis', 'overwrite')
    
    # 2. Find correlations
    if len(numeric_cols) >= 2:
        target_col = numeric_cols[0]
        correlations = find_top_correlations(df, target_col)
        print(f'Top correlations with {target_col}:')
        for col, corr in correlations:
            print(f'{col}: {corr:.3f}')
    
    # 3. Detect anomalies if there are numeric columns
    if numeric_cols:
        value_col = numeric_cols[0]
        anomalies_df = identify_anomalies(df, value_col)
        anomalies_count = anomalies_df.filter(anomalies_df.is_anomaly == True).count()
        print(f'Detected {anomalies_count} anomalies in {value_col}')
        
        # Write results to BigQuery
        integration.write_to_bigquery(anomalies_df, 'analysis_results.anomalies', 'overwrite')
    
    # Create reporting visualizations
    print('Generating reports...')
    reporting = SparkReporting()
    
    # Convert Spark DataFrame to Pandas for visualization
    pandas_df = reporting.spark_df_to_pandas(df.limit(1000))
    
    # Generate charts for reporting
    charts = []
    if len(numeric_cols) >= 2 and len(pandas_df) > 0:
        # Create scatter plot
        scatter_path = reporting.create_scatter_plot(
            pandas_df, 
            numeric_cols[0], 
            numeric_cols[1], 
            f'Relationship between {numeric_cols[0]} and {numeric_cols[1]}'
        )
        charts.append(scatter_path)
    
    if len(categorical_cols) > 0 and len(numeric_cols) > 0 and len(pandas_df) > 0:
        # Create bar chart
        pandas_df_grouped = pandas_df.groupby(categorical_cols[0])[numeric_cols[0]].mean().reset_index()
        bar_path = reporting.create_bar_chart(
            pandas_df_grouped.head(10), 
            categorical_cols[0], 
            numeric_cols[0], 
            f'Average {numeric_cols[0]} by {categorical_cols[0]}'
        )
        charts.append(bar_path)
    
    # Create HTML report
    if charts:
        report_path = reporting.create_html_report(
            'BigQuery-Spark Data Analysis Report',
            f'Analysis of {QUERY_LIMIT} records from {DATASET}',
            charts=charts,
            tables=[(f'Sample data from {DATASET}', pandas_df.head(10))]
        )
        print(f'Report generated: {report_path}')
        
    # Stop Spark session
    integration.stop()
    print('Analysis completed successfully!')
    
except Exception as e:
    print(f'Error: {str(e)}')
    sys.exit(1)
"

    if [ $? -eq 0 ]; then
        print_message "BigQuery-Spark analysis completed successfully!"
    else
        print_error "Analysis encountered an error. Check the logs for details."
    fi
}

# Display help
show_help() {
    echo "BigQuery-Spark Integration Script"
    echo
    echo "Usage: ./run.sh [command]"
    echo
    echo "Commands:"
    echo "  setup     Install requirements and create directories"
    echo "  run       Run the BigQuery-Spark integration workflow"
    echo "  help      Display this help message"
    echo
    echo "Without arguments, the script will run the full workflow."
}

# Main execution
case "$1" in
    setup)
        check_requirements
        create_directories
        ;;
    run)
        run_integration
        ;;
    help)
        show_help
        ;;
    *)
        check_requirements
        create_directories
        run_integration
        ;;
esac

print_message "Done!"