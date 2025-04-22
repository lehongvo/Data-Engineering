FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for GCP credentials if using service account
RUN mkdir -p /app/credentials

# Use ARG for build-time variables
ARG PORT=8080

# Expose port
EXPOSE ${PORT}

# Set environment variable to indicate we're in a Docker container
ENV IS_DOCKER=true

# Run the application with gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT} app:app