#!/bin/bash

# Output colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Message display functions
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check required tools
check_requirements() {
    print_message "Checking required tools..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    # Check awslocal
    if ! command -v awslocal &> /dev/null; then
        print_error "awslocal is not installed. Please run: pip install awscli-local"
        exit 1
    fi
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Get S3 URL for an object
get_s3_url() {
    local bucket_name=$1
    local file_name=$(basename "$2")
    echo "http://localhost:4566/$bucket_name/$file_name"
}

# Validate bucket name
validate_bucket_name() {
    local bucket_name=$1
    if [[ ! $bucket_name =~ ^[a-z0-9][a-z0-9.-]*[a-z0-9]$ ]]; then
        print_error "Invalid bucket name. Bucket name must:"
        echo "- Contain only lowercase letters, numbers, dots, and hyphens"
        echo "- Begin and end with a letter or number"
        echo "- Be between 3-63 characters long"
        return 1
    fi
    if [ ${#bucket_name} -lt 3 ] || [ ${#bucket_name} -gt 63 ]; then
        print_error "Bucket name must be between 3-63 characters long"
        return 1
    fi
    return 0
}

# Initialize clean environment
init_environment() {
    print_warning "Cleaning up old environment..."
    
    # Stop running container if exists
    if [ "$(docker ps -q -f name=localstack-main)" ]; then
        print_message "Stopping running localstack-main container..."
        docker stop localstack-main
    fi
    
    # Remove old container if exists
    if [ "$(docker ps -aq -f name=localstack-main)" ]; then
        print_message "Removing old localstack-main container..."
        docker rm localstack-main
    fi
    
    print_message "Environment cleaned"
}

# Start LocalStack
start_localstack() {
    print_message "Starting LocalStack..."
    docker run -d --name localstack-main -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
    
    # Wait for LocalStack to be ready
    print_message "Waiting for LocalStack to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s localhost:4566 > /dev/null; then
            print_message "LocalStack is ready"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_error "LocalStack failed to start after ${max_attempts} seconds"
    cleanup
    exit 1
}

# Create bucket
create_bucket() {
    if [ -z "$1" ]; then
        print_error "Please provide a bucket name"
        return 1
    fi
    
    if ! validate_bucket_name "$1"; then
        return 1
    fi
    
    print_message "Creating bucket $1..."
    if awslocal s3 mb s3://$1 2>&1 | grep -q "make_bucket failed"; then
        print_error "Failed to create bucket $1"
        return 1
    fi
    print_message "Successfully created bucket $1"
    print_message "Bucket URL: http://localhost:4566/$1"
}

# Upload file to bucket
upload_file() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        print_error "Please provide file path and bucket name"
        echo "Usage: upload_file <file_path> <bucket_name>"
        return 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "File $1 does not exist"
        return 1
    fi
    
    print_message "Uploading file $1 to bucket $2..."
    if ! awslocal s3 cp "$1" "s3://$2/"; then
        print_error "File upload failed"
        return 1
    fi
    
    local file_name=$(basename "$1")
    local s3_url=$(get_s3_url "$2" "$1")
    print_message "File upload successful"
    print_message "File URL: $s3_url"
}

# List bucket contents
list_bucket() {
    if [ -z "$1" ]; then
        print_message "Listing all buckets:"
        awslocal s3 ls
    else
        print_message "Listing contents of bucket $1:"
        awslocal s3 ls "s3://$1"
        print_message "Bucket URL: http://localhost:4566/$1"
    fi
}

# Delete bucket and contents
delete_bucket() {
    if [ -z "$1" ]; then
        print_error "Please provide a bucket name"
        return 1
    fi
    print_warning "Deleting bucket $1 and all its contents..."
    if ! awslocal s3 rb "s3://$1" --force; then
        print_error "Failed to delete bucket $1"
        return 1
    fi
    print_message "Successfully deleted bucket $1"
}

# Clean up environment
cleanup() {
    print_warning "Cleaning up environment..."
    if [ "$(docker ps -q -f name=localstack-main)" ]; then
        docker stop localstack-main
        docker rm localstack-main
    fi
    print_message "Cleanup complete"
}

# Show menu
show_menu() {
    echo -e "\n${GREEN}=== S3 MANAGEMENT MENU ===${NC}"
    echo "1. Start LocalStack"
    echo "2. Create new bucket"
    echo "3. Upload file"
    echo "4. List buckets/contents"
    echo "5. Delete bucket"
    echo "6. Clean environment"
    echo "0. Exit"
    echo -n "Your choice: "
}

# Main loop
main() {
    check_requirements
    check_docker
    init_environment
    
    while true; do
        show_menu
        read choice
        case $choice in
            1) start_localstack ;;
            2) 
                echo -n "Enter bucket name: "
                read bucket_name
                create_bucket "$bucket_name"
                ;;
            3)
                echo -n "Enter file path: "
                read file_path
                echo -n "Enter bucket name: "
                read bucket_name
                upload_file "$file_path" "$bucket_name"
                ;;
            4)
                echo -n "Enter bucket name (leave empty to list all): "
                read bucket_name
                list_bucket "$bucket_name"
                ;;
            5)
                echo -n "Enter bucket name to delete: "
                read bucket_name
                delete_bucket "$bucket_name"
                ;;
            6) 
                cleanup
                init_environment
                ;;
            0) 
                cleanup
                print_message "Goodbye!"
                exit 0
                ;;
            *) print_error "Invalid choice" ;;
        esac
    done
}

# Run script
main 