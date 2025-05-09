#!/bin/bash

# Script to set up BigQuery for streaming pipeline

echo "===== BigQuery Setup ====="

# Check Google Cloud SDK 
if ! command -v gcloud &> /dev/null; then
    echo "Google Cloud SDK is not installed. Please install it first."
    exit 1
fi

# Request project information
read -p "Enter Google Cloud Project ID: " PROJECT_ID
read -p "Enter Dataset ID (default: clickstream_analytics): " DATASET_ID
DATASET_ID=${DATASET_ID:-clickstream_analytics}
read -p "Enter table name (default: user_page_stats): " TABLE_NAME
TABLE_NAME=${TABLE_NAME:-user_page_stats}

# Set up project
echo "Setting up Google Cloud project: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Create dataset if it doesn't exist
echo "Creating BigQuery Dataset $DATASET_ID"
bq --location=US mk --dataset $PROJECT_ID:$DATASET_ID

# Create table
echo "Creating BigQuery Table $TABLE_NAME"
bq mk --table $PROJECT_ID:$DATASET_ID.$TABLE_NAME \
    user_id:STRING,page:STRING,view_count:INTEGER,avg_session_duration:FLOAT,last_activity:STRING

# Create service account for Flink
echo "Creating service account for Flink"
SERVICE_ACCOUNT="flink-bigquery-sa"
gcloud iam service-accounts create $SERVICE_ACCOUNT \
    --display-name="Flink BigQuery Service Account"

# Grant permissions to service account
echo "Granting permissions to service account"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

# Create key for service account
echo "Creating key file for service account"
gcloud iam service-accounts keys create ./data/bigquery-service-account.json \
    --iam-account=$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

echo "===== BigQuery Setup Complete! ====="
echo "Service account key file: ./data/bigquery-service-account.json"
echo "Project ID: $PROJECT_ID"
echo "Dataset ID: $DATASET_ID"
echo "Table name: $TABLE_NAME"
echo ""
echo "Please update this information in the flink_processor.py file" 