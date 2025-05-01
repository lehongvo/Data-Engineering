#!/bin/bash

# Exit on error
set -e

echo "Setting up virtual environment for Token Data API..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the API server
echo "Starting API server..."
echo "API will be available at http://localhost:8000"
python main.py