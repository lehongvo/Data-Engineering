#!/bin/bash

# Setup Python virtual environment
python3 -m venv vapf
source vapf/bin/activate

# BigQuery Partitioning Exercise Runner
# This script sets up and runs all the examples for the BigQuery partitioning exercise
# Created: May 2, 2025

echo "================================================="
echo "BigQuery Partitioning Exercise Runner"
echo "================================================="

# Check if we're authenticated with Google Cloud
echo "Checking Google Cloud authentication..."
gcloud auth list --filter=status:ACTIVE --format="value(account)" || {
    echo "You need to authenticate with Google Cloud first. Run:"
    echo "gcloud auth login"
    exit 1
}

# Get the current project ID
PROJECT_ID=$(gcloud config get-value project)
echo "Current project ID: $PROJECT_ID"

# Check if the PROJECT_ID is empty
if [ -z "$PROJECT_ID" ]; then
    echo "No project ID was found. Please set your Google Cloud project ID:"
    echo "gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

# Create directory for output data if it doesn't exist
mkdir -p data

# Install required Python packages - with improved error handling
echo "Installing required Python packages..."

# Install packages in virtual environment
pip install google-cloud-bigquery pandas matplotlib

# Verify that the packages were installed successfully
echo "Verifying package installation..."
python -c "from google.cloud import bigquery; import pandas; import matplotlib; print('All required packages installed successfully!')" || {
    echo "Package verification failed. Please install the required packages manually:"
    echo "pip install google-cloud-bigquery pandas matplotlib"
    exit 1
}

# Update the Python scripts with the current project ID
echo "Updating Python scripts with your project ID: $PROJECT_ID"
sed -i '' "s/your-project-id/$PROJECT_ID/g" create_partitioned_table.py partition_metadata.py
sed -i '' "s/your-project-id/$PROJECT_ID/g" sample_queries.sql

# Make scripts executable
chmod +x create_partitioned_table.py partition_metadata.py

# Run the BigQuery partitioning examples
echo "================================================="
echo "1. Creating partitioned tables in BigQuery..."
echo "================================================="
python create_partitioned_table.py

echo ""
echo "================================================="
echo "2. Analyzing partition metadata..."
echo "================================================="
python partition_metadata.py

echo ""
echo "================================================="
echo "3. Sample queries you can run in BigQuery console"
echo "================================================="
echo "Check sample_queries.sql for optimized query examples"
echo "These queries demonstrate how to use partition filters for performance optimization"
echo ""

echo "================================================="
echo "Exercise completed!"
echo "================================================="
echo ""
echo "Next steps:"
echo "1. Review the visualizations in the data/ directory"
echo "2. Try running the sample queries in the Google BigQuery console"
echo "3. Experiment with creating your own partitioned tables"
echo ""
echo "For more information on BigQuery partitioning, visit:"
echo "https://cloud.google.com/bigquery/docs/partitioned-tables"

# Deactivate virtual environment when done
deactivate