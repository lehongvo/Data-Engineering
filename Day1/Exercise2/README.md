# Flask BigQuery Docker Application

This project demonstrates a Flask application that integrates with Google BigQuery, containerized using Docker, and deployed on a Google Cloud Platform (GCP) Virtual Machine.

## Project Structure
```
Exercise2/
├── app.py              # Main Flask application with BigQuery integration
├── requirements.txt    # Python dependencies
├── Dockerfile          # Instructions for building Docker image
├── docker-compose.yml  # Docker services configuration
├── .env                # Environment variables (local) - not in git
├── .env.example        # Example environment variables template
├── templates/          # HTML templates
│   └── index.html      # Main page template
└── static/             # Static files (CSS, JS, images)
```

## Prerequisites

- Google Cloud Platform account with billing enabled
- Google Cloud SDK installed
- Docker & Docker Compose installed
- A GCP Service Account with BigQuery permissions

## Local Development Setup

1. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` with your GCP configuration:
   ```
   GCP_PROJECT_ID=your-gcp-project-id
   GOOGLE_APPLICATION_CREDENTIALS=./credentials/your-service-account-key.json
   ```

3. Create a credentials directory and place your GCP service account key:
```bash
mkdir -p credentials
# Place your service account JSON key file in the credentials directory
```

4. Run the application locally:
```bash
flask run
```

## Docker Setup (Local)

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8080`

## Deployment to GCP VM

### Option 1: Manual VM Setup

1. Create a GCP VM instance:
   - Go to the GCP Console
   - Navigate to Compute Engine > VM instances
   - Click "Create Instance"
   - Choose a machine type (e.g., e2-small)
   - Check "Allow HTTP/HTTPS traffic"
   - Click "Create"

2. Connect to your VM using SSH:
```bash
gcloud compute ssh your-vm-name --project your-project-id --zone your-zone
```

3. Install Docker and Docker Compose on the VM:
```bash
# Update package lists
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to Docker group
sudo usermod -aG docker $USER
```

4. Log out and log back in for group changes to take effect:
```bash
exit
gcloud compute ssh your-vm-name --project your-project-id --zone your-zone
```

5. Clone your repository on the VM:
```bash
git clone your-repository-url
cd Exercise2
```

6. Set up environment variables and credentials:
```bash
cp .env.example .env
# Edit .env with your project ID
nano .env

# Create credentials directory
mkdir -p credentials
```

7. Create a service account key file on your local machine and copy it to the VM:
```bash
# On local machine
gcloud compute scp your-service-account-key.json your-vm-name:~/Exercise2/credentials/ --project your-project-id --zone your-zone
```

8. Run the application with Docker Compose:
```bash
docker-compose up -d
```

### Option 2: Using Terraform (Infrastructure as Code)

For automated deployment, you can use Terraform to provision the GCP VM and deploy your application. See examples in the Terraform documentation.

## API Endpoints

- GET `/`: Web interface to test BigQuery connection
- GET `/api/health`: Health check endpoint
- GET `/api/bigquery/test`: Test BigQuery connection and run a sample query

## Environment Variables

- `PORT`: Application port (default: 8080)
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Debug mode (1/0)
- `GCP_PROJECT_ID`: Your Google Cloud project ID
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your GCP service account key file

**Note**: Never commit `.env` file or service account keys to Git. Always use `.env.example` as a template.

## Security Best Practices

1. **Service Account Permissions**: Use least privilege principles when creating service accounts
2. **Environment Variables**: Store sensitive information in environment variables, not in code
3. **Firewall Rules**: Configure GCP firewall to limit access to your VM
4. **Regular Updates**: Keep dependencies updated to address security vulnerabilities

## Performance Optimization

1. **BigQuery Query Optimization**: Use efficient queries to minimize processing costs
2. **Caching**: Implement caching for frequent queries using Redis or Memcached
3. **Connection Pooling**: Reuse BigQuery connections where possible

## Troubleshooting

1. **GCP Authentication Issues**
   - Verify your service account key is properly set up
   - Check if the service account has the necessary permissions

2. **Docker Issues**
   - Check logs: `docker-compose logs`
   - Verify ports are properly exposed

3. **Application Errors**
   - Check Flask logs
   - Verify environment variables are correctly set

## Resources

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)