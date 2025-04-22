#!/bin/bash

# Exit on any error
set -e

# Variables
PROJECT_ID="unique-axle-457602-n6"
ZONE="asia-southeast1-a"
INSTANCE_NAME="flask-bigquery-app"
MACHINE_TYPE="e2-medium"

# Create VM instance
echo "Creating VM instance..."
gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=411826471488-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20240223,mode=rw,size=10,type=projects/$PROJECT_ID/zones/$ZONE/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=env=prod

# Wait for VM to be ready
echo "Waiting for VM to be ready..."
sleep 30

# Install Docker and dependencies
echo "Installing Docker and dependencies..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
    sudo apt-get update && \
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    sudo apt-get update && \
    sudo apt-get install -y docker-ce docker-compose && \
    sudo usermod -aG docker $USER
'

# Create necessary directories on VM
echo "Creating directories..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
    mkdir -p ~/app/credentials
'

# Copy application files
echo "Copying application files..."
gcloud compute scp --recurse ./* $INSTANCE_NAME:~/app --zone=$ZONE

# Copy .env file separately
echo "Copying .env file..."
gcloud compute scp .env $INSTANCE_NAME:~/app/.env --zone=$ZONE

# Start application
echo "Starting application..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
    cd ~/app && \
    sudo docker-compose up -d
'

echo "Deployment completed successfully!"
echo "Application should be running at: http://$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)'):8080" 