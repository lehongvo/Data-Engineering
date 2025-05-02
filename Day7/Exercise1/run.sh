#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to compare versions
version_compare() {
    if [[ $1 == $2 ]]
    then
        echo "="
    elif [[ $1 == $(echo -e "$1\n$2" | sort -V | head -n1) ]]
    then
        echo "<"
    else
        echo ">"
    fi
}

# Function to install Python packages with error handling
install_packages() {
    echo -e "${GREEN}Upgrading pip...${NC}"
    pip install --upgrade pip

    echo -e "${GREEN}Installing setuptools and wheel first...${NC}"
    pip install --upgrade setuptools wheel

    echo -e "${GREEN}Installing other required packages...${NC}"
    if ! pip install -r requirements.txt; then
        echo -e "${RED}Failed to install required packages${NC}"
        echo -e "${RED}Trying to install packages one by one...${NC}"
        
        while IFS= read -r package || [[ -n "$package" ]]; do
            # Skip empty lines and comments
            [[ $package =~ ^[[:space:]]*$ ]] && continue
            [[ $package =~ ^#.*$ ]] && continue
            
            echo -e "${GREEN}Installing $package...${NC}"
            if ! pip install "$package"; then
                echo -e "${RED}Failed to install $package${NC}"
                exit 1
            fi
        done < requirements.txt
    fi
}

# Function to setup service account key
setup_service_account() {
    # Create config directory if it doesn't exist
    mkdir -p "$SCRIPT_DIR/config"
    
    # Check possible locations for service account key
    POSSIBLE_LOCATIONS=(
        "../config/cgp-service-account-key.json"
        "../../config/cgp-service-account-key.json"
        "./config/cgp-service-account-key.json"
        "$HOME/config/cgp-service-account-key.json"
    )
    
    KEY_FOUND=false
    for SOURCE_KEY in "${POSSIBLE_LOCATIONS[@]}"; do
        if [ -f "$SOURCE_KEY" ]; then
            echo -e "${GREEN}Found service account key at: $SOURCE_KEY${NC}"
            cp "$SOURCE_KEY" "$SERVICE_ACCOUNT_KEY"
            chmod 400 "$SERVICE_ACCOUNT_KEY"
            KEY_FOUND=true
            break
        fi
    done
    
    if [ "$KEY_FOUND" = false ]; then
        echo -e "${YELLOW}Service account key not found in common locations.${NC}"
        echo -e "${BLUE}Checking if logged into gcloud and trying to create key...${NC}"
        
        # Check if the user is logged into gcloud
        if gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
            echo -e "${GREEN}Creating a new service account key...${NC}"
            # Create a new service account if needed
            SERVICE_ACCOUNT_NAME="bigquery-api-service"
            SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
            
            # Check if the service account already exists
            if ! gcloud iam service-accounts describe ${SERVICE_ACCOUNT_EMAIL} &> /dev/null; then
                echo -e "${BLUE}Creating new service account: ${SERVICE_ACCOUNT_EMAIL}${NC}"
                gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
                    --display-name="BigQuery API Service Account" \
                    --description="Service account for BigQuery API"
                
                # Grant necessary permissions
                echo -e "${BLUE}Granting BigQuery permissions...${NC}"
                gcloud projects add-iam-policy-binding ${PROJECT_ID} \
                    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
                    --role="roles/bigquery.admin"
            else
                echo -e "${GREEN}Service account already exists: ${SERVICE_ACCOUNT_EMAIL}${NC}"
            fi
            
            # Create a new key
            echo -e "${BLUE}Generating new service account key...${NC}"
            gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_KEY} \
                --iam-account=${SERVICE_ACCOUNT_EMAIL}
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Service account key created successfully at: ${SERVICE_ACCOUNT_KEY}${NC}"
                chmod 400 "$SERVICE_ACCOUNT_KEY"
                KEY_FOUND=true
            else
                echo -e "${RED}Failed to create service account key.${NC}"
            fi
        fi
    fi
    
    if [ "$KEY_FOUND" = false ]; then
        echo -e "${RED}Could not create or find service account key.${NC}"
        echo -e "${BLUE}Please place your service account key in one of these locations and try again:${NC}"
        for loc in "${POSSIBLE_LOCATIONS[@]}"; do
            echo -e "${BLUE}- $loc${NC}"
        done
        echo -e "${BLUE}Or set GOOGLE_APPLICATION_CREDENTIALS manually:${NC}"
        echo -e "${BLUE}export GOOGLE_APPLICATION_CREDENTIALS=\"path/to/your/cgp-service-account-key.json\"${NC}"
        exit 1
    fi
    
    # Export GOOGLE_APPLICATION_CREDENTIALS
    export GOOGLE_APPLICATION_CREDENTIALS="$SERVICE_ACCOUNT_KEY"
    echo -e "${GREEN}GOOGLE_APPLICATION_CREDENTIALS set to: $GOOGLE_APPLICATION_CREDENTIALS${NC}"
}

# Function to update SQL queries with project ID
update_queries() {
    local project_id=$1
    echo -e "${GREEN}Updating SQL queries with project ID: $project_id${NC}"
    
    # Replace PROJECT_ID in all SQL files
    find "$SCRIPT_DIR/queries" -name "*.sql" -type f -exec sed -i.bak "s/PROJECT_ID/$project_id/g" {} \;
    find "$SCRIPT_DIR/queries" -name "*.bak" -type f -delete
}

# Function to set up required APIs
setup_apis() {
    echo -e "${GREEN}Setting up required Google Cloud APIs...${NC}"
    
    # List of APIs to enable
    APIS=(
        "bigquery.googleapis.com"
        "cloudbuild.googleapis.com"
        "cloudfunctions.googleapis.com"
        "run.googleapis.com"
        "artifactregistry.googleapis.com"
        "secretmanager.googleapis.com"
    )
    
    for api in "${APIS[@]}"; do
        if ! gcloud services list --enabled --filter="name:$api" --format="value(name)" &> /dev/null; then
            echo -e "${BLUE}Enabling $api...${NC}"
            gcloud services enable $api
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}$api enabled successfully!${NC}"
            else
                echo -e "${RED}Failed to enable $api. Please enable it manually.${NC}"
            fi
        else
            echo -e "${GREEN}$api is already enabled.${NC}"
        fi
    done
}

# Function to verify Cloud Build configuration
verify_cloud_build() {
    echo -e "\n${YELLOW}=== VERIFYING CLOUD BUILD CONFIGURATION ===${NC}"
    
    # Check if Cloud Build API is enabled
    echo -e "${GREEN}Checking if Cloud Build API is enabled...${NC}"
    if ! gcloud services list --enabled --filter="name:cloudbuild.googleapis.com" --format="value(name)" &> /dev/null; then
        echo -e "${RED}Cloud Build API is not enabled. Enabling now...${NC}"
        gcloud services enable cloudbuild.googleapis.com
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to enable Cloud Build API. Check permissions for your account.${NC}"
            return 1
        fi
    else
        echo -e "${GREEN}Cloud Build API is already enabled.${NC}"
    fi
    
    # Verify project existence and permissions
    echo -e "${GREEN}Verifying project existence and permissions...${NC}"
    if ! gcloud projects describe "$PROJECT_ID" &> /dev/null; then
        echo -e "${RED}Project $PROJECT_ID does not exist or you don't have access to it.${NC}"
        echo -e "${BLUE}Available projects for your account:${NC}"
        gcloud projects list --format="table(projectId,name)"
        
        echo -e "${GREEN}Enter a valid Project ID to use:${NC}"
        read -r NEW_PROJECT_ID
        
        gcloud config set project "$NEW_PROJECT_ID"
        PROJECT_ID="$NEW_PROJECT_ID"
        echo -e "${GREEN}Project set to: ${BLUE}$PROJECT_ID${NC}"
    else
        echo -e "${GREEN}Project $PROJECT_ID exists and you have access.${NC}"
    fi
    
    # Verify Secret Manager setup
    echo -e "${GREEN}Verifying Secret Manager configuration...${NC}"
    if ! gcloud services list --enabled --filter="name:secretmanager.googleapis.com" --format="value(name)" &> /dev/null; then
        echo -e "${RED}Secret Manager API is not enabled. Enabling now...${NC}"
        gcloud services enable secretmanager.googleapis.com
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to enable Secret Manager API. Check permissions for your account.${NC}"
            return 1
        fi
    else
        echo -e "${GREEN}Secret Manager API is already enabled.${NC}"
    fi
    
    # Check if the secret exists
    if ! gcloud secrets describe "bigquery-api-service-account" &> /dev/null; then
        echo -e "${YELLOW}Secret 'bigquery-api-service-account' not found.${NC}"
        echo -e "${GREEN}Creating Secret Manager secret for service account key...${NC}"
        
        if [ ! -f "$SERVICE_ACCOUNT_KEY" ]; then
            echo -e "${RED}Service account key not found at: $SERVICE_ACCOUNT_KEY${NC}"
            setup_service_account
        fi
        
        # Create the secret with service account key content
        if ! cat "$SERVICE_ACCOUNT_KEY" | gcloud secrets create "bigquery-api-service-account" --data-file=- &> /dev/null; then
            echo -e "${RED}Failed to create secret 'bigquery-api-service-account'.${NC}"
            echo -e "${BLUE}Manual steps:${NC}"
            echo -e "1. Create a secret in Secret Manager named 'bigquery-api-service-account'"
            echo -e "2. Upload your service account key to this secret"
            echo -e "${BLUE}gcloud secrets create bigquery-api-service-account --data-file=path/to/key.json${NC}"
            return 1
        else
            echo -e "${GREEN}Secret 'bigquery-api-service-account' created successfully.${NC}"
        fi
    else
        echo -e "${GREEN}Secret 'bigquery-api-service-account' already exists.${NC}"
    fi
    
    # Verify Cloud Build service account permissions
    echo -e "${GREEN}Verifying Cloud Build service account permissions...${NC}"
    
    # Get Cloud Build service account
    CLOUDBUILD_SA="$(gcloud projects get-iam-policy $PROJECT_ID --format='value(bindings.members)' | grep cloudbuild.gserviceaccount.com | head -1 | sed 's/serviceAccount://')"
    
    if [ -z "$CLOUDBUILD_SA" ]; then
        CLOUDBUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"
        echo -e "${YELLOW}Could not find Cloud Build service account, using default: $CLOUDBUILD_SA${NC}"
    else
        echo -e "${GREEN}Found Cloud Build service account: $CLOUDBUILD_SA${NC}"
    fi
    
    # Add required permissions to Cloud Build service account
    echo -e "${GREEN}Ensuring Cloud Build service account has necessary permissions...${NC}"
    
    # Required roles for Cloud Build
    REQUIRED_ROLES=(
        "roles/cloudbuild.builds.builder"
        "roles/secretmanager.secretAccessor"
        "roles/run.admin"
        "roles/storage.admin"
        "roles/bigquery.admin"
        "roles/iam.serviceAccountUser"
    )
    
    for role in "${REQUIRED_ROLES[@]}"; do
        echo -e "${GREEN}Adding role $role to Cloud Build service account...${NC}"
        gcloud projects add-iam-policy-binding $PROJECT_ID \
            --member="serviceAccount:$CLOUDBUILD_SA" \
            --role="$role" --quiet
        
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}Warning: Could not add role $role to Cloud Build service account.${NC}"
            echo -e "${BLUE}You might need to add this role manually.${NC}"
        fi
    done
    
    return 0
}

# Function to directly configure Secret Manager and Cloud Build
setup_cloud_build_secret() {
    echo -e "\n${YELLOW}=== CONFIGURING SECRET MANAGER AND CLOUD BUILD ===${NC}"
    
    local project_id=$1
    
    # Create the secret directly using service account key
    echo -e "${GREEN}Checking if bigquery-api-service-account secret exists...${NC}"
    if ! gcloud secrets describe bigquery-api-service-account --project="$project_id" &> /dev/null; then
        echo -e "${YELLOW}Secret 'bigquery-api-service-account' not found. Creating it now...${NC}"
        
        # Make sure the service account key exists
        if [ ! -f "$SERVICE_ACCOUNT_KEY" ]; then
            echo -e "${RED}Service account key not found at: $SERVICE_ACCOUNT_KEY${NC}"
            echo -e "${BLUE}Setting up service account...${NC}"
            setup_service_account
        fi
        
        # Create the secret
        echo -e "${GREEN}Creating secret from service account key...${NC}"
        cat "$SERVICE_ACCOUNT_KEY" | gcloud secrets create bigquery-api-service-account \
            --project="$project_id" \
            --replication-policy="automatic" \
            --data-file=- \
            --quiet
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create secret. Creating with explicit value...${NC}"
            
            # Create an empty secret first
            gcloud secrets create bigquery-api-service-account \
                --project="$project_id" \
                --replication-policy="automatic" \
                --quiet
                
            # Then update the secret version
            cat "$SERVICE_ACCOUNT_KEY" | gcloud secrets versions add bigquery-api-service-account \
                --project="$project_id" \
                --data-file=- \
                --quiet
        fi
    else
        echo -e "${GREEN}Secret 'bigquery-api-service-account' already exists.${NC}"
    fi
    
    # Get project number for default service account
    PROJECT_NUMBER=$(gcloud projects describe "$project_id" --format="value(projectNumber)")
    
    # Configure Cloud Build service account with required permissions
    echo -e "${GREEN}Setting up Cloud Build service account permissions...${NC}"
    
    # Default Cloud Build service account
    CLOUDBUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"
    
    echo -e "${GREEN}Using Cloud Build service account: $CLOUDBUILD_SA${NC}"
    
    # Required roles for Cloud Build
    REQUIRED_ROLES=(
        "roles/cloudbuild.builds.builder"
        "roles/secretmanager.secretAccessor"
        "roles/run.admin"
        "roles/storage.admin"
        "roles/bigquery.admin"
        "roles/iam.serviceAccountUser"
    )
    
    for role in "${REQUIRED_ROLES[@]}"; do
        echo -e "${GREEN}Adding role $role to Cloud Build service account...${NC}"
        gcloud projects add-iam-policy-binding "$project_id" \
            --member="serviceAccount:$CLOUDBUILD_SA" \
            --role="$role" \
            --quiet
    done
    
    echo -e "${GREEN}Cloud Build service account configured successfully!${NC}"
    
    # Show how to run Cloud Build manually
    echo -e "\n${YELLOW}To run Cloud Build manually, use:${NC}"
    echo -e "${BLUE}gcloud builds submit --config=cloudbuild.yaml --project=$project_id${NC}"
}

# Function to build and deploy using Docker and Google Cloud
build_and_deploy() {
    echo -e "\n${YELLOW}=== STARTING BUILD AND DEPLOYMENT ===${NC}"
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
        echo -e "${BLUE}Visit: https://docs.docker.com/get-docker/${NC}"
        exit 1
    fi
    
    # Check if user is logged in to Docker
    if ! docker info &> /dev/null; then
        echo -e "${RED}Not logged in to Docker. Please run:${NC}"
        echo -e "${BLUE}docker login${NC}"
        exit 1
    fi
    
    # Always build Docker image
    echo -e "${GREEN}Building Docker image...${NC}"
    if ! docker build -t bigquery-api:latest .; then
        echo -e "${RED}Docker build failed.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Docker image built successfully!${NC}"
    
    # Check if user wants to deploy to Google Cloud
    echo -e "${GREEN}Do you want to deploy to Google Cloud? [Y/n]${NC}"
    read -r cloud_choice
    
    if [[ -z "$cloud_choice" || "$cloud_choice" =~ ^[Yy]$ ]]; then
        # Check if gcloud is installed
        if ! command -v gcloud &> /dev/null; then
            echo -e "${RED}Google Cloud SDK is not installed. Please install it first.${NC}"
            echo -e "${BLUE}Visit: https://cloud.google.com/sdk/docs/install${NC}"
            exit 1
        fi
        
        # Check if user is logged in to gcloud
        if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
            echo -e "${RED}Not logged in to Google Cloud. Please run:${NC}"
            echo -e "${BLUE}gcloud auth login${NC}"
            exit 1
        fi
        
        # Configure Docker for Google Container Registry
        echo -e "${GREEN}Configuring Docker for Google Container Registry...${NC}"
        gcloud auth configure-docker --quiet
        
        # Verify Cloud Build configuration
        verify_cloud_build
        
        # Check if user wants to use Cloud Build
        echo -e "${GREEN}Do you want to use Cloud Build instead of local Docker build? [y/N]${NC}"
        read -r cloudbuild_choice
        
        if [[ "$cloudbuild_choice" =~ ^[Yy]$ ]]; then
            # Use Cloud Build to build and deploy
            echo -e "${GREEN}Starting Cloud Build process...${NC}"
            if gcloud builds submit --config=cloudbuild.yaml .; then
                echo -e "${GREEN}Cloud Build completed successfully!${NC}"
                APP_URL=$(gcloud run services describe bigquery-api --platform managed --region us-central1 --format="value(status.url)")
                echo -e "${GREEN}Your application is available at:${NC} ${BLUE}$APP_URL${NC}"
            else
                echo -e "${RED}Cloud Build failed.${NC}"
                exit 1
            fi
        else
            # Use local Docker build and deploy to Cloud Run
            echo -e "${GREEN}Building image for Google Container Registry with platform linux/amd64...${NC}"
            if ! docker buildx create --use --name multiarch-builder &>/dev/null; then
                echo -e "${BLUE}Multiarch builder already exists${NC}"
            fi
            
            if ! docker buildx build --platform linux/amd64 -t "gcr.io/$PROJECT_ID/bigquery-api:latest" --push .; then
                echo -e "${RED}Docker build for linux/amd64 failed.${NC}"
                echo -e "${YELLOW}Trying alternative method with standard build...${NC}"
                
                # Alternative method if buildx fails
                docker build -t bigquery-api:latest .
                
                echo -e "${GREEN}Tagging image for Google Container Registry...${NC}"
                docker tag bigquery-api:latest "gcr.io/$PROJECT_ID/bigquery-api:latest"
                
                echo -e "${GREEN}Pushing image to Google Container Registry...${NC}"
                if ! docker push "gcr.io/$PROJECT_ID/bigquery-api:latest"; then
                    echo -e "${RED}Failed to push image to Google Container Registry.${NC}"
                    exit 1
                fi
            fi
            
            echo -e "${GREEN}Deploying to Cloud Run...${NC}"
            if ! gcloud run deploy bigquery-api \
                --image "gcr.io/$PROJECT_ID/bigquery-api:latest" \
                --platform managed \
                --region us-central1 \
                --allow-unauthenticated \
                --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
                --memory 512Mi; then
                echo -e "${RED}Failed to deploy to Cloud Run.${NC}"
                exit 1
            fi
            
            echo -e "${GREEN}Deployment successful!${NC}"
            echo -e "${GREEN}Your application is now available at:${NC}"
            APP_URL=$(gcloud run services describe bigquery-api --platform managed --region us-central1 --format="value(status.url)")
            echo -e "${BLUE}$APP_URL${NC}"
        fi
        
        # Log thông tin chi tiết về instance đang chạy
        echo -e "\n${YELLOW}=== INSTANCE DETAILS ===${NC}"
        echo -e "${GREEN}Fetching instance details...${NC}"
        gcloud run services describe bigquery-api --platform managed --region us-central1 --format="yaml"
        
        # Log thông tin về các revision
        echo -e "\n${YELLOW}=== REVISION HISTORY ===${NC}"
        gcloud run revisions list --service bigquery-api --platform managed --region us-central1
        
        # Log thông tin về tình trạng hiện tại
        echo -e "\n${YELLOW}=== CURRENT STATUS ===${NC}"
        gcloud run services get-iam-policy bigquery-api --platform managed --region us-central1
        
        echo -e "\n${GREEN}Logs for the deployed instance can be viewed with:${NC}"
        echo -e "${BLUE}gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=bigquery-api' --limit=10${NC}"
        
        # Lưu thông tin triển khai vào file
        echo -e "\n${GREEN}Saving deployment information to deployment-info.log${NC}"
        {
            echo "Deployment Time: $(date)"
            echo "Project ID: $PROJECT_ID"
            echo "Application URL: $APP_URL"
            echo "Service: bigquery-api"
            echo "Region: us-central1"
            echo "Image: gcr.io/$PROJECT_ID/bigquery-api:latest"
        } > "deployment-info.log"
    else
        echo -e "${BLUE}Skipping Google Cloud deployment.${NC}"
        echo -e "${GREEN}You can run the Docker image locally with:${NC}"
        echo -e "${BLUE}docker run -p 8000:8000 -e GOOGLE_APPLICATION_CREDENTIALS=/app/config/cgp-service-account-key.json -v $GOOGLE_APPLICATION_CREDENTIALS:/app/config/cgp-service-account-key.json bigquery-api:latest${NC}"
    fi
}

# Main script execution starts here
echo -e "${YELLOW}===============================${NC}"
echo -e "${GREEN}BigQuery API Setup and Deployment${NC}"
echo -e "${YELLOW}===============================${NC}"

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"

# Check if Python version is compatible (>= 3.8)
MIN_VERSION="3.8"
if [[ $(version_compare "$PYTHON_VERSION" "$MIN_VERSION") == "<" ]]; then
    echo -e "${RED}Python version must be 3.8 or higher${NC}"
    exit 1
fi

# Set service account key path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVICE_ACCOUNT_KEY="$SCRIPT_DIR/config/cgp-service-account-key.json"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Google Cloud SDK (gcloud) is not installed. Please install it first:${NC}"
    echo -e "${BLUE}https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

# Check if bq is installed
if ! command -v bq &> /dev/null; then
    echo -e "${RED}BigQuery CLI (bq) is not installed. Please install Google Cloud SDK with BigQuery component:${NC}"
    echo -e "${BLUE}gcloud components install bq${NC}"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}jq is not installed. Installing it now...${NC}"
    
    # Attempt to install jq based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install jq
        else
            echo -e "${RED}Homebrew not found. Please install jq manually:${NC}"
            echo -e "${BLUE}brew install jq${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y jq
        elif command -v yum &> /dev/null; then
            sudo yum install -y jq
        else
            echo -e "${RED}Package manager not found. Please install jq manually.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Unsupported OS. Please install jq manually.${NC}"
        exit 1
    fi
fi

# Check if user is logged in to gcloud
echo -e "\n${GREEN}Checking Google Cloud authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}Not logged in to Google Cloud. Initiating login process...${NC}"
    gcloud auth login
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to log in to Google Cloud. Please run manually:${NC}"
        echo -e "${BLUE}gcloud auth login${NC}"
        exit 1
    fi
fi

# Get current project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
echo -e "${GREEN}Current Project ID: ${BLUE}$PROJECT_ID${NC}"

# Check if project ID is set
if [ -z "$PROJECT_ID" ]; then
    echo -e "${YELLOW}No project ID configured. Please select a project:${NC}"
    
    # List available projects
    gcloud projects list --format="table(projectId,name)"
    
    # Prompt user to select project
    echo -e "${GREEN}Enter the Project ID to use:${NC}"
    read -r PROJECT_ID
    
    # Set the project
    gcloud config set project "$PROJECT_ID"
    
    echo -e "${GREEN}Project set to: ${BLUE}$PROJECT_ID${NC}"
fi

# Update SQL queries with project ID
update_queries "$PROJECT_ID"

# Setup required Google Cloud APIs
setup_apis

# Check if dataset exists, if not create it
echo -e "\n${GREEN}Checking if dataset exists...${NC}"
if ! bq ls "${PROJECT_ID}:exercise1" &>/dev/null; then
    echo -e "${BLUE}Creating dataset exercise1...${NC}"
    bq mk --dataset "${PROJECT_ID}:exercise1"
fi

# Check and delete all tables in the exercise1 dataset
echo -e "\n${GREEN}Checking for existing tables in exercise1 dataset...${NC}"
TABLES=$(bq ls -n 1000 "${PROJECT_ID}:exercise1" 2>/dev/null | grep -v "TableId" | awk '{print $1}')
if [ -n "$TABLES" ]; then
    echo -e "${BLUE}Found existing tables. Deleting all tables in exercise1 dataset...${NC}"
    for table in $TABLES; do
        echo -e "${BLUE}Deleting table: $table${NC}"
        bq rm -f "${PROJECT_ID}:exercise1.$table"
    done
    echo -e "${GREEN}All tables deleted successfully!${NC}"
else
    echo -e "${GREEN}No existing tables found in exercise1 dataset.${NC}"
fi

# Ask if the user wants to proceed with development or build directly
echo -e "\n${YELLOW}How do you want to proceed?${NC}"
echo -e "1) ${GREEN}Set up development environment${NC}"
echo -e "2) ${BLUE}Build and deploy directly${NC}"
read -r -p "Enter your choice (1/2): " proceed_choice

if [ "$proceed_choice" = "1" ]; then
    # Set up development environment
    
    # Remove existing virtual environment if it exists
    if [ -d "venv" ]; then
        echo -e "${GREEN}Removing existing virtual environment...${NC}"
        rm -rf venv
    fi
    
    # Create new virtual environment
    echo -e "\n${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
    
    # Activate virtual environment
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source venv/bin/activate
    
    # Install packages with error handling
    install_packages
    
    # Check if GOOGLE_APPLICATION_CREDENTIALS is set
    if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        echo -e "${GREEN}Setting up service account credentials...${NC}"
        setup_service_account
    fi
    
    # Verify service account key exists and is valid
    if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        echo -e "${RED}Service account key file not found at: $GOOGLE_APPLICATION_CREDENTIALS${NC}"
        setup_service_account
    fi
    
    # Verify service account key is valid JSON
    if ! jq empty "$GOOGLE_APPLICATION_CREDENTIALS" 2>/dev/null; then
        echo -e "${RED}Service account key file is not valid JSON${NC}"
        setup_service_account
    fi
    
    # Create necessary directories if they don't exist
    echo -e "\n${GREEN}Creating necessary directories...${NC}"
    mkdir -p data
    mkdir -p queries
    mkdir -p api/config
    mkdir -p config
    
    # Make main.py executable
    chmod +x main.py
    
    # Ask user if they want to run in development mode or build and deploy
    echo -e "\n${YELLOW}How do you want to run the application?${NC}"
    echo -e "1) ${GREEN}Run in development mode${NC}"
    echo -e "2) ${BLUE}Build and deploy${NC}"
    read -r -p "Enter your choice (1/2): " choice
    
    if [ "$choice" = "1" ]; then
        # Start the application in development mode
        echo -e "\n${GREEN}Starting BigQuery API application in development mode...${NC}"
        echo -e "${GREEN}API documentation will be available at: http://localhost:8000/docs${NC}"
        
        # Run the main.py script without importing sample data
        python main.py --reload
    elif [ "$choice" = "2" ]; then
        # Build and deploy
        build_and_deploy
    else
        echo -e "${RED}Invalid choice. Please run the script again and select 1 or 2.${NC}"
        exit 1
    fi
elif [ "$proceed_choice" = "2" ]; then
    # Set up service account credentials since they will be needed for deployment
    if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ] || [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        echo -e "${GREEN}Setting up service account credentials...${NC}"
        setup_service_account
    fi
    
    # Create necessary directories if they don't exist
    echo -e "\n${GREEN}Creating necessary directories...${NC}"
    mkdir -p data
    mkdir -p queries
    mkdir -p api/config
    mkdir -p config
    
    # Proceed directly to build and deploy
    build_and_deploy
else
    echo -e "${RED}Invalid choice. Please run the script again and select 1 or 2.${NC}"
    exit 1
fi