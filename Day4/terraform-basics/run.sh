#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

# Project ID
PROJECT_ID="unique-axle-457602-n6"

# Function to check for errors
check_error() {
    if [ $? -ne 0 ]; then
        print_message $RED "❌ Error: $1"
        exit 1
    fi
}

# Function to delete VM instance specifically
delete_vm_instance() {
    print_message $YELLOW "🗑️ Checking and deleting VM instance if exists..."
    
    # Check if instance exists
    if gcloud compute instances describe data-engineering-practice-dev-data-processing-instance \
        --zone=asia-southeast1-a \
        --project=$PROJECT_ID &>/dev/null; then
        
        print_message $YELLOW "🗑️ Deleting existing VM instance..."
        gcloud compute instances delete data-engineering-practice-dev-data-processing-instance \
            --zone=asia-southeast1-a \
            --project=$PROJECT_ID \
            --quiet
        
        # Wait for 30 seconds to ensure the instance is fully deleted
        print_message $YELLOW "⏳ Waiting for VM instance to be fully deleted..."
        sleep 30
    else
        print_message $GREEN "✅ No existing VM instance found."
    fi
}

# Function to clean up existing Python environment
cleanup_python_env() {
    print_message $YELLOW "🧹 Cleaning up existing Python environment..."
    
    # Check if we're in a virtual environment and deactivate if so
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        deactivate
    fi
    
    # Remove existing venv if it exists
    if [ -d "scripts/venv" ]; then
        print_message $YELLOW "🗑️ Removing existing virtual environment..."
        rm -rf scripts/venv
    fi
}

# Function to setup Python environment and run data loading script
setup_and_run_python() {
    # Clean up existing environment first
    cleanup_python_env
    
    print_message $YELLOW "🐍 Setting up new Python environment..."
    
    # Create and activate virtual environment
    cd scripts
    python3 -m venv venv
    check_error "Failed to create virtual environment"
    
    source venv/bin/activate
    check_error "Failed to activate virtual environment"
    
    # Install requirements
    print_message $YELLOW "📦 Installing Python dependencies..."
    pip install -r ../requirements.txt
    check_error "Failed to install Python dependencies"
    
    # Run the script
    print_message $YELLOW "🔄 Loading sample data..."
    python3 load_sample_data.py
    check_error "Failed to load sample data"
    
    # Deactivate virtual environment
    deactivate
    cd ..
    
    print_message $GREEN "✅ Successfully loaded sample data!"
}

# Function to create firewall rule
create_firewall_rule() {
    print_message $YELLOW "🔒 Creating firewall rule for SSH access..."
    
    # Check if firewall rule exists
    if gcloud compute firewall-rules describe data-engineering-practice-dev-allow-ssh \
        --project=$PROJECT_ID &>/dev/null; then
        print_message $YELLOW "🗑️ Deleting existing firewall rule..."
        gcloud compute firewall-rules delete data-engineering-practice-dev-allow-ssh \
            --project=$PROJECT_ID \
            --quiet
    fi
    
    print_message $YELLOW "🔥 Creating new firewall rule..."
    gcloud compute firewall-rules create data-engineering-practice-dev-allow-ssh \
        --project=$PROJECT_ID \
        --network=data-engineering-practice-dev-vpc \
        --allow=tcp:22 \
        --source-ranges=0.0.0.0/0 \
        --target-tags=data-processing \
        --description="Allow SSH access to VM instances" \
        --quiet
        
    check_error "Failed to create firewall rule"
}

# Function to delete firewall rule
delete_firewall_rule() {
    print_message $YELLOW "🔥 Checking and deleting firewall rule if exists..."
    
    # Check if firewall rule exists
    if gcloud compute firewall-rules describe data-engineering-practice-dev-allow-ssh \
        --project=$PROJECT_ID &>/dev/null; then
        print_message $YELLOW "🗑️ Deleting firewall rule..."
        gcloud compute firewall-rules delete data-engineering-practice-dev-allow-ssh \
            --project=$PROJECT_ID \
            --quiet
    else
        print_message $GREEN "✅ No existing firewall rule found."
    fi
}

# 1. Delete all infrastructure
delete_infrastructure() {
    print_message $YELLOW "🗑️ Deleting all infrastructure..."
    
    # Set credentials
    export GOOGLE_APPLICATION_CREDENTIALS="/Users/user/Desktop/Data-Engineering/Day4/config/cgp-service-account-key.json"
    check_error "Failed to set credentials"

    # First delete VM instance specifically
    delete_vm_instance

    # Delete firewall rule before other resources
    delete_firewall_rule

    # First, disable deletion protection
    print_message $YELLOW "🔓 Disabling deletion protection..."
    
    # Update main.tf to disable deletion protection
    sed -i '' 's/deletion_protection = true/deletion_protection = false/' main.tf 2>/dev/null || \
    sed -i 's/deletion_protection = true/deletion_protection = false/' main.tf
    
    # If deletion_protection line doesn't exist, add it
    if ! grep -q "deletion_protection" main.tf; then
        sed -i '' '/table_id.*"raw_sales_data"/a\
        deletion_protection = false' main.tf 2>/dev/null || \
        sed -i '/table_id.*"raw_sales_data"/a\  deletion_protection = false' main.tf
    fi
    
    # Apply the changes first
    print_message $YELLOW "🔄 Applying deletion protection changes..."
    terraform apply -auto-approve -var="project_id=$PROJECT_ID"
    check_error "Failed to apply deletion protection changes"
    
    # Now destroy infrastructure
    print_message $YELLOW "💥 Destroying infrastructure..."
    terraform destroy -auto-approve -var="project_id=$PROJECT_ID"
    check_error "Failed to destroy infrastructure"
    
    print_message $GREEN "✅ Successfully deleted all infrastructure!"
}

# 2. Recreate infrastructure
create_infrastructure() {
    print_message $YELLOW "🚀 Creating new infrastructure..."
    
    # Init
    print_message $YELLOW "📦 Initializing Terraform..."
    terraform init
    check_error "Failed to initialize Terraform"
    
    # Plan
    print_message $YELLOW "📋 Planning changes..."
    terraform plan -var="project_id=$PROJECT_ID"
    check_error "Failed to create plan"
    
    # Apply
    print_message $YELLOW "🏗️ Applying changes..."
    terraform apply -auto-approve -var="project_id=$PROJECT_ID"
    check_error "Failed to apply changes"
    
    # Wait for network to be fully created
    print_message $YELLOW "⏳ Waiting for network to be fully created..."
    sleep 30
    
    # Create firewall rule using gcloud
    create_firewall_rule
    
    print_message $GREEN "✅ Successfully created new infrastructure!"
}

# Main script
print_message $YELLOW "🔄 Starting infrastructure reset process..."

# 1. Delete old infrastructure
delete_infrastructure

# Wait for 2 minutes to ensure all permissions are properly propagated
print_message $YELLOW "⏳ Waiting for 2 minutes to ensure permissions are properly propagated..."
sleep 20

# 2. Create new infrastructure
create_infrastructure

# 3. Load sample data
setup_and_run_python

print_message $GREEN "🎉 Done! Infrastructure has been successfully reset and sample data loaded!"

# Print verification links
print_message $YELLOW "\n🔍 Verify your infrastructure at these links:"
print_message $BLUE "VPC Networks: https://console.cloud.google.com/networking/networks"
print_message $BLUE "Cloud Storage: https://console.cloud.google.com/storage"
print_message $BLUE "BigQuery: https://console.cloud.google.com/bigquery"
print_message $BLUE "VM Instances: https://console.cloud.google.com/compute/instances"

# Print resource names for easy verification
print_message $YELLOW "\n📋 Resource names to check:"
print_message $GREEN "VPC Network: data-engineering-practice-dev-vpc"
print_message $GREEN "Subnet: data-engineering-practice-dev-subnet"
print_message $GREEN "Storage Bucket: data-engineering-practice-data-lake-dev"
print_message $GREEN "BigQuery Dataset: data_engineering_practice_dev"
print_message $GREEN "BigQuery Table: raw_sales_data"
print_message $GREEN "VM Instance: data-engineering-practice-dev-data-processing-instance"
