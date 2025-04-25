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

# 1. Delete all infrastructure
delete_infrastructure() {
    print_message $YELLOW "🗑️ Deleting all infrastructure..."
    
    # Set credentials
    export GOOGLE_APPLICATION_CREDENTIALS="/Users/user/Desktop/Data-Engineering/Day4/***REMOVED***"
    check_error "Failed to set credentials"

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
    
    print_message $GREEN "✅ Successfully created new infrastructure!"
}

# Main script
print_message $YELLOW "🔄 Starting infrastructure reset process..."

# 1. Delete old infrastructure
delete_infrastructure

# 2. Create new infrastructure
create_infrastructure

print_message $GREEN "🎉 Done! Infrastructure has been successfully reset!"

# Print verification links
print_message $YELLOW "\n🔍 Verify your infrastructure at these links:"
print_message $BLUE "VPC Networks: https://console.cloud.google.com/networking/networks"
print_message $BLUE "Cloud Storage: https://console.cloud.google.com/storage"
print_message $BLUE "BigQuery: https://console.cloud.google.com/bigquery"

# Print resource names for easy verification
print_message $YELLOW "\n📋 Resource names to check:"
print_message $GREEN "VPC Network: data-engineering-practice-dev-vpc"
print_message $GREEN "Subnet: data-engineering-practice-dev-subnet"
print_message $GREEN "Storage Bucket: data-engineering-practice-data-lake-dev"
print_message $GREEN "BigQuery Dataset: data_engineering_practice_dev"
print_message $GREEN "BigQuery Table: raw_sales_data"
