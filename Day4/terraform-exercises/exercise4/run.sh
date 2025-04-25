#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_ID="unique-axle-457602-n6"
PROJECT_NAME="data-pipeline"
ENVIRONMENT="dev"
USER_EMAIL="lehongvi19x@gmail.com"

# Function to print colored messages
print_message() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check for errors
check_error() {
    if [ $? -ne 0 ]; then
        print_message $RED "❌ Error: $1"
        exit 1
    fi
}

# Function to check and set up authentication
setup_auth() {
    print_message $YELLOW "🔑 Checking authentication..."
    
    # Get current account
    current_account=$(gcloud config get-value account)
    
    # If not logged in or wrong account, do login
    if [ "$current_account" != "$USER_EMAIL" ]; then
        print_message $YELLOW "Logging in as $USER_EMAIL..."
        gcloud auth login $USER_EMAIL
        check_error "Failed to login"
        
        # Set project
        print_message $YELLOW "Setting project..."
        gcloud config set project $PROJECT_ID
        check_error "Failed to set project"
    else
        print_message $GREEN "Already logged in as $USER_EMAIL"
    fi
}

# Function to deploy infrastructure
deploy_infrastructure() {
    # First, ensure we're using the right account
    setup_auth
    
    # Initialize Terraform
    print_message $YELLOW "📦 Initializing Terraform..."
    terraform init
    check_error "Failed to initialize Terraform"

    # Plan the changes
    print_message $YELLOW "📋 Planning infrastructure changes..."
    terraform plan -out=tfplan
    check_error "Failed to create plan"

    # Apply the changes
    print_message $YELLOW "🏗️ Applying infrastructure changes..."
    terraform apply tfplan
    check_error "Failed to apply changes"

    # Clean up the plan file
    rm tfplan

    print_message $GREEN "✅ Infrastructure has been successfully created/updated!"

    # Print resource information
    print_message $YELLOW "\n📋 Resource Information:"
    terraform output

    # Save service account key to file
    print_message $YELLOW "\n🔑 Saving service account key..."
    terraform output -raw service_account_key > service-account-key.json 2>/dev/null || true
    
    if [ -f "service-account-key.json" ]; then
        print_message $GREEN "✅ Service account key saved to service-account-key.json"
    else
        print_message $YELLOW "⚠️ No new service account key was generated (using existing one)"
    fi
}

# Function to test Pub/Sub
test_pubsub() {
    setup_auth
    
    print_message $YELLOW "🔄 Testing Pub/Sub functionality..."
    
    # Get topic and subscription names
    topic_name=$(terraform output -raw pubsub_topic)
    subscription_name=$(terraform output -raw pubsub_subscription)
    
    # Publish a test message
    print_message $YELLOW "📤 Publishing test message..."
    echo "Hello from data pipeline $(date)" | gcloud pubsub topics publish $topic_name --message-body="$(cat -)"
    check_error "Failed to publish message"
    
    # Pull the message
    print_message $YELLOW "📥 Pulling message..."
    gcloud pubsub subscriptions pull $subscription_name --auto-ack --limit=1
    check_error "Failed to pull message"
    
    print_message $GREEN "✅ Pub/Sub test completed successfully!"
}

# Function to test storage buckets
test_storage() {
    setup_auth
    
    print_message $YELLOW "🗄️ Testing storage functionality..."
    
    # Get bucket names
    data_lake_bucket=$(terraform output -raw data_lake_bucket)
    temp_bucket=$(terraform output -raw temp_bucket)
    
    # Create test files
    echo "Test data for data lake" > test_data.txt
    echo "Test data for temp storage" > test_temp.txt
    
    # Upload to data lake
    print_message $YELLOW "📤 Uploading to data lake bucket..."
    gsutil cp test_data.txt gs://$data_lake_bucket/
    check_error "Failed to upload to data lake"
    
    # Upload to temp bucket
    print_message $YELLOW "📤 Uploading to temp bucket..."
    gsutil cp test_temp.txt gs://$temp_bucket/
    check_error "Failed to upload to temp bucket"
    
    # List contents
    print_message $YELLOW "\n📋 Data Lake Bucket Contents:"
    gsutil ls -l gs://$data_lake_bucket/
    
    print_message $YELLOW "\n📋 Temp Bucket Contents:"
    gsutil ls -l gs://$temp_bucket/
    
    # Clean up
    rm test_data.txt test_temp.txt
    
    print_message $GREEN "✅ Storage test completed successfully!"
}

# Function to test VPC connectivity
test_vpc() {
    setup_auth
    
    print_message $YELLOW "🌐 Testing VPC network connectivity..."
    
    # Get network and subnet names
    network_name=$(terraform output -raw vpc_network)
    subnet_name=$(terraform output -raw vpc_subnet)
    
    # List firewall rules
    print_message $YELLOW "\n📋 Firewall Rules:"
    gcloud compute firewall-rules list --filter="network:$network_name" --format="table(name,network,direction,priority,sourceRanges.list():label=SRC_RANGES,destinationRanges.list():label=DEST_RANGES)"
    
    # Test VPC connector
    print_message $YELLOW "\n🔌 VPC Connector Status:"
    connector_name=$(terraform output -raw vpc_connector)
    gcloud compute networks vpc-access connectors describe $connector_name --region=$(gcloud config get-value region)
    
    print_message $GREEN "✅ VPC network test completed successfully!"
}

# Function to destroy infrastructure
destroy_infrastructure() {
    setup_auth
    
    print_message $YELLOW "⚠️ This will destroy all infrastructure. Are you sure? (y/N)"
    read -p "" confirm
    
    if [ "$confirm" != "y" ]; then
        print_message $YELLOW "Aborted."
        return
    fi
    
    print_message $YELLOW "🗑️ Destroying infrastructure..."
    terraform destroy -auto-approve
    check_error "Failed to destroy infrastructure"

    print_message $GREEN "✅ Infrastructure has been successfully destroyed!"
}

# Main menu loop
while true; do
    print_message $YELLOW "\nData Pipeline Infrastructure Management"
    print_message $YELLOW "Please select an option:"
    print_message $GREEN "1) Deploy/Update Infrastructure"
    print_message $GREEN "2) Test Pub/Sub"
    print_message $GREEN "3) Test Storage"
    print_message $GREEN "4) Test VPC Network"
    print_message $GREEN "5) Destroy Infrastructure"
    print_message $GREEN "6) Exit"
    read -p "Enter your choice (1-6): " choice

    case $choice in
        1)
            deploy_infrastructure
            ;;
        2)
            test_pubsub
            ;;
        3)
            test_storage
            ;;
        4)
            test_vpc
            ;;
        5)
            destroy_infrastructure
            ;;
        6)
            print_message $GREEN "👋 Goodbye!"
            exit 0
            ;;
        *)
            print_message $RED "❌ Invalid choice. Please select 1-6."
            ;;
    esac
done 