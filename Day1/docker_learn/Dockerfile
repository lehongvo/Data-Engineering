# Use official Python base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Use environment variable for port
ENV PORT=8080

# Expose port
EXPOSE ${PORT}

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app