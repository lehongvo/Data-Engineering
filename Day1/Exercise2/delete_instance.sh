#!/bin/bash

# Variables
PROJECT_ID="unique-axle-457602-n6"
ZONE="asia-southeast1-a"
INSTANCE_NAME="flask-bigquery-app"

# Delete the instance
echo "Deleting VM instance..."
gcloud compute instances delete $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --quiet

echo "Instance deleted successfully!" 