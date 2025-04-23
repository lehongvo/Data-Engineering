# Flask BigQuery Application

## Overview
This application provides a web interface to interact with Google BigQuery, featuring automatic data insertion via a cron job. It includes both a web service and a background job service.

## Prerequisites
- Google Cloud Platform Account
- Python 3.9+
- Docker and Docker Compose
- Google Cloud SDK
- A GCP Project with BigQuery API enabled
- Service Account with BigQuery permissions

## Project Structure
```
.
├── app.py              # Main Flask application
├── cron_insert.py      # Background job for data insertion
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker services configuration
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS)
└── templates/         # HTML templates
```

## Environment Variables
Create a `.env` file with the following variables:
```
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
API_KEY_INSERT=your-api-key
```

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Google Cloud credentials:
- Download your service account key file
- Rename it to `credentials.json`
- Place it in the project root directory

5. Run the application:
```bash
python app.py
```

## Docker Deployment

1. Build and start the containers:
```bash
docker-compose build
docker-compose up -d
```

2. Check container status:
```bash
docker-compose ps
```

3. View logs:
```bash
# Web application logs
docker-compose logs web

# Cron job logs
docker-compose logs cronjob
```

## Google Cloud Deployment

1. Create a Compute Engine instance:
```bash
gcloud compute instances create flask-bigquery-app \
    --zone=asia-southeast1-a \
    --machine-type=e2-medium \
    --tags=http-server \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud
```

2. Set up firewall rule:
```bash
gcloud compute firewall-rules create allow-flask-app \
    --allow tcp:8080 \
    --target-tags=http-server \
    --description="Allow incoming traffic on TCP port 8080"
```

3. SSH into the instance:
```bash
gcloud compute ssh flask-bigquery-app --zone=asia-southeast1-a
```

4. Install Docker and Docker Compose on the instance:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

5. Deploy the application:
```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create .env file and add credentials
nano .env

# Start the application
docker-compose up -d
```

## Redeployment Process

### 1. Delete Existing Instance
```bash
# Navigate to project directory
cd path/to/project

# Run delete instance script
./delete_instance.sh
```
This script will:
- Delete the VM instance named 'flask-bigquery-app'
- Clean up associated resources
- Provide feedback on deletion status

### 2. Deploy New Instance
```bash
# Run deployment script
./deploy.sh
```
The deployment script will:
- Create a new VM instance
- Set up necessary firewall rules
- Install Docker and dependencies
- Clone and configure the application
- Start the Docker containers

### 3. Verify Deployment
After deployment, verify the application:

1. Access the web interface:
```bash
# Use the instance's external IP
http://<instance-ip>:8080
```

2. Check container status:
```bash
gcloud compute ssh flask-bigquery-app --zone=asia-southeast1-a --project=your-project-id \
    --command="cd ~/app && docker-compose ps"
```

3. View application logs:
```bash
# Check web application logs
gcloud compute ssh flask-bigquery-app --zone=asia-southeast1-a --project=your-project-id \
    --command="cd ~/app && docker-compose logs web"

# Check cron job logs
gcloud compute ssh flask-bigquery-app --zone=asia-southeast1-a --project=your-project-id \
    --command="cd ~/app && docker-compose logs cronjob"
```

4. Test functionality:
   - Add new records through the web interface
   - Verify pagination works
   - Check if cron job is inserting data (view logs)
   - Test search and filter features

### 4. Troubleshooting Deployment
If issues occur during deployment:

1. SSH into the instance:
```bash
gcloud compute ssh flask-bigquery-app --zone=asia-southeast1-a --project=your-project-id
```

2. Common checks:
```bash
# Check Docker status
sudo systemctl status docker

# View Docker containers
docker ps

# Check application directory
cd ~/app
ls -la

# View Docker Compose logs
docker-compose logs

# Check environment variables
cat .env
```

3. Common issues and solutions:
   - If containers aren't running: `docker-compose up -d`
   - If permission issues: Check credentials.json and .env file
   - If network issues: Verify firewall rules
   - If data not showing: Check BigQuery connection and permissions

## API Endpoints

- `GET /`: Main web interface
- `GET /health`: Health check endpoint
- `GET /test`: Test BigQuery connection
- `POST /insert`: Insert records into BigQuery
- `GET /records`: Retrieve records with filtering and pagination

## Features

1. Web Interface:
   - Form for manual data insertion
   - Table view of existing records
   - Filtering by name and age range
   - Pagination support

2. Background Job:
   - Automatic insertion of random records
   - Configurable schedule (default: every hour)
   - Detailed logging in `cron_insert.log`

3. Security:
   - API key validation
   - Google Cloud authentication
   - Firewall rules configuration

## Monitoring

1. Application Logs:
```bash
# View web application logs
docker-compose logs web

# View cron job logs
docker-compose logs cronjob

# View cron job log file
cat cron_insert.log
```

2. BigQuery Monitoring:
- Access BigQuery console to monitor:
  - Query execution
  - Data insertion
  - Table updates

## Troubleshooting

1. Connection Issues:
- Verify firewall rules are properly configured
- Check if the application is running: `docker-compose ps`
- Verify the instance's external IP is accessible

2. BigQuery Issues:
- Verify service account permissions
- Check credentials file location
- Review application logs for specific errors

3. Cron Job Issues:
- Check cron_insert.log for errors
- Verify API key in .env file
- Check BigQuery permissions

## Support

For issues and support:
1. Check the logs first
2. Review the troubleshooting section
3. Contact the development team

## License
[Your License Information]