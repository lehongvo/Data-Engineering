#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_ID="unique-axle-457602-n6"
PROJECT_NAME="data-lake"
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

    print_message $YELLOW "\n🔍 You can verify your resources in the Google Cloud Console:"
    print_message $GREEN "Cloud Storage: https://console.cloud.google.com/storage"
    print_message $GREEN "BigQuery: https://console.cloud.google.com/bigquery"
    print_message $GREEN "IAM & Admin: https://console.cloud.google.com/iam-admin"
}

# Function to upload a file to the bucket
upload_file() {
    # First, ensure we're using the right account
    setup_auth
    
    if [ -z "$1" ]; then
        print_message $RED "❌ Please provide a file path to upload"
        exit 1
    fi

    local file_path=$1
    if [ ! -f "$file_path" ]; then
        print_message $RED "❌ File not found: $file_path"
        exit 1
    fi

    bucket_name=$(terraform output -raw bucket_name)
    print_message $YELLOW "📤 Uploading file to bucket: $bucket_name"
    
    gsutil cp "$file_path" "gs://$bucket_name/"
    check_error "Failed to upload file"
    
    # Get the filename from the path
    filename=$(basename "$file_path")
    
    print_message $GREEN "✅ File uploaded successfully!"
    print_message $YELLOW "\n🔍 Access your uploaded file:"
    print_message $GREEN "Console: https://console.cloud.google.com/storage/browser/_details/$bucket_name/$filename"
    print_message $GREEN "Direct link: gs://$bucket_name/$filename"
}

# Function to list bucket contents
list_bucket() {
    # First, ensure we're using the right account
    setup_auth
    
    bucket_name=$(terraform output -raw bucket_name)
    print_message $YELLOW "📋 Listing contents of bucket: $bucket_name"
    
    # Get the bucket listing
    print_message $YELLOW "\nFiles in bucket:"
    gsutil ls -l "gs://$bucket_name" | while read -r line; do
        if [[ $line =~ gs://* ]]; then
            file_path=$line
            filename=$(basename "$file_path")
            print_message $GREEN "📄 $line"
            print_message $YELLOW "  Console: https://console.cloud.google.com/storage/browser/_details/$bucket_name/$filename"
        else
            print_message $NC "$line"
        fi
    done
    
    print_message $YELLOW "\n🔍 View bucket in Console:"
    print_message $GREEN "https://console.cloud.google.com/storage/browser/$bucket_name"
}

# Function to test BigQuery access
test_bigquery() {
    # First, ensure we're using the right account
    setup_auth
    
    dataset_id=$(terraform output -raw dataset_id)
    print_message $YELLOW "🔍 Testing BigQuery access for dataset: $dataset_id"
    
    # List tables in the dataset
    print_message $YELLOW "\nListing tables in dataset..."
    bq ls "$PROJECT_ID:$dataset_id"
    check_error "Failed to list tables"
    
    # Create a sample table with data
    print_message $YELLOW "\nCreating a sample table with data..."
    echo '{"name":"John", "age":30}
{"name":"Alice", "age":25}' > sample_data.json
    
    bq load --source_format=NEWLINE_DELIMITED_JSON \
        "$dataset_id.sample_table" \
        sample_data.json \
        name:STRING,age:INTEGER
    
    # Query the sample data
    print_message $YELLOW "\nQuerying sample data:"
    bq query --use_legacy_sql=false \
        "SELECT * FROM \`$PROJECT_ID.$dataset_id.sample_table\`"
    
    print_message $GREEN "✅ BigQuery access test completed successfully!"
    print_message $YELLOW "\n🔍 View dataset in Console:"
    print_message $GREEN "https://console.cloud.google.com/bigquery?project=$PROJECT_ID&d=$dataset_id&p=$PROJECT_ID&page=dataset"
    
    # Clean up
    rm -f sample_data.json
}

# Function to destroy infrastructure
destroy_infrastructure() {
    # First, ensure we're using the right account
    setup_auth
    
    print_message $YELLOW "⚠️ This will destroy all infrastructure. Are you sure? (y/N)"
    read -p "" confirm
    
    if [ "$confirm" != "y" ]; then
        print_message $YELLOW "Aborted."
        return
    fi
    
    # Delete infrastructure
    print_message $YELLOW "🗑️ Destroying infrastructure..."
    terraform destroy -auto-approve
    check_error "Failed to destroy infrastructure"

    print_message $GREEN "✅ Infrastructure has been successfully destroyed!"
}

# Main menu loop
while true; do
    print_message $YELLOW "\nWelcome to Data Lake Management Script"
    print_message $YELLOW "Please select an option:"
    print_message $GREEN "1) Deploy/Update Infrastructure"
    print_message $GREEN "2) Upload File to Bucket"
    print_message $GREEN "3) List Bucket Contents"
    print_message $GREEN "4) Test BigQuery Access"
    print_message $GREEN "5) Destroy Infrastructure"
    print_message $GREEN "6) Exit"
    read -p "Enter your choice (1-6): " choice

    case $choice in
        1)
            deploy_infrastructure
            ;;
        2)
            read -p "Enter the path to the file you want to upload: " file_path
            upload_file "$file_path"
            ;;
        3)
            list_bucket
            ;;
        4)
            test_bigquery
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