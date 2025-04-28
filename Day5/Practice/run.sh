#!/bin/bash

PROJECT_ID="unique-axle-457602-n6"
REGION="asia-southeast1"
ZONE="asia-southeast1-b"
BUCKET_NAME="bucket-test-${PROJECT_ID}-$(date +%Y%m%d%H%M%S)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_message() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

check_error() {
    if [ $? -ne 0 ]; then
        print_message $RED "❌ Error: $1"
        exit 1
    fi
}

print_message $YELLOW "🧹 Cleaning up Docker containers, images, networks, volumes..."
docker rm -f etl-api etl-postgres 2>/dev/null || true
docker container prune -f
docker image prune -a -f
docker network prune -f
docker volume prune -f

print_message $YELLOW "🧹 Cleaning up ALL GCS buckets in project $PROJECT_ID..."
for bucket in $(gsutil ls -p $PROJECT_ID); do
    print_message $YELLOW "Deleting $bucket ..."
    gsutil -m rm -r $bucket || true
    print_message $GREEN "Deleted $bucket"
done

POSTGRES_PORT=5432
if lsof -i :5432 >/dev/null 2>&1; then
    POSTGRES_PORT=5433
    print_message $YELLOW "⚠️ Port 5432 is busy. Using port 5433 for Postgres."
else
    print_message $YELLOW "✅ Using port 5432 for Postgres."
fi

API_PORT=5000
if lsof -i :5000 >/dev/null 2>&1; then
    API_PORT=5001
    print_message $YELLOW "⚠️ Port 5000 is busy. Using port 5001 for ETL API."
else
    print_message $YELLOW "✅ Using port 5000 for ETL API."
fi

print_message $YELLOW "📦 Initializing Terraform..."
cd terraform
terraform init
check_error "Failed to initialize Terraform"

print_message $YELLOW "🏗️ Applying infrastructure (Terraform)..."
terraform apply -auto-approve -var="project=$PROJECT_ID" -var="region=$REGION" -var="zone=$ZONE" -var="bucket_name=$BUCKET_NAME"
print_message $YELLOW "✅ Instance link: https://console.cloud.google.com/compute/instances?project=$PROJECT_ID"
print_message $GREEN "✅ Bucket link: https://console.cloud.google.com/storage/browser?project=$PROJECT_ID"
check_error "Failed to apply Terraform"

# Lấy tên bucket từ terraform output
ACTUAL_BUCKET_NAME=$(terraform output -raw bucket_name)
print_message $GREEN "📦 Created bucket: $ACTUAL_BUCKET_NAME"
cd ..

print_message $YELLOW "🐳 Building Docker image for ETL API..."
docker build -t etl-api -f docker/Dockerfile .
check_error "Failed to build Docker image"

print_message $YELLOW "🐘 Starting Postgres DB container on port $POSTGRES_PORT..."
docker run -d --name etl-postgres --rm -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=etldb -p $POSTGRES_PORT:5432 postgres:13
check_error "Failed to start Postgres container"

print_message $YELLOW "🚀 Starting ETL API container (Flask) on port $API_PORT..."
docker run -d --name etl-api --rm \
  -p $API_PORT:5000 \
  -v $(pwd)/***REMOVED***:/gcp-service-account-key.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/gcp-service-account-key.json \
  -e BUCKET_NAME=$ACTUAL_BUCKET_NAME \
  etl-api
check_error "Failed to start ETL API container"

print_message $GREEN "✅ Deploy successfully! ETL API is ready at http://localhost:$API_PORT"
print_message $GREEN "📦 Using bucket: $ACTUAL_BUCKET_NAME"

print_message $YELLOW "🚀 Initialize App Engine for the project (if not already present)..."
gcloud app create --region=$REGION --quiet || true

print_message $YELLOW "🚀 Deploying ETL API lên Google App Engine..."

# Create file app.yaml 
cat > ./etl/app.yaml <<EOL
runtime: python39
instance_class: F1

entrypoint: gunicorn -b :\$PORT etl_api:app

env_variables:
  BUCKET_NAME: "$ACTUAL_BUCKET_NAME"
  GOOGLE_APPLICATION_CREDENTIALS: "cgp-service-account-key.json"

handlers:
- url: /.*
  script: auto
  secure: always

includes:
- .env.yaml
EOL

# Create requirements.txt for App Engine
cat > ./etl/requirements.txt <<EOL
Flask==2.0.1
gunicorn==20.1.0
google-cloud-storage==2.5.0
google-cloud-bigquery==2.34.3
pandas==1.4.2
python-dotenv==0.19.2
EOL

# Copy credentials to etl/ if needed
cp ./***REMOVED*** ./etl/cgp-service-account-key.json

# Create .env.yaml for App Engine environment variables
cat > ./etl/.env.yaml <<EOL
env_variables:
  GOOGLE_APPLICATION_CREDENTIALS: "cgp-service-account-key.json"
EOL

# Deploy to App Engine
cd etl
gcloud app deploy app.yaml --quiet
cd ..

# Get URL of App Engine after deployment
APP_URL=$(gcloud app browse --no-launch-browser)
print_message $GREEN "✅ App Engine deploy successfully!"
print_message $GREEN "🌐 API URL: $APP_URL"
print_message $GREEN "📦 Bucket: $ACTUAL_BUCKET_NAME"

# Show logs for debugging
print_message $YELLOW "📝 Checking App Engine logs..."
gcloud app logs tail -s default 