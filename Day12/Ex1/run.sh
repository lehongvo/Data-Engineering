#!/bin/bash

echo "==== DBT E-commerce Project Setup ===="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker before continuing."
    exit 1
fi

# Check docker-compose or docker compose
DOCKER_COMPOSE_CMD=""
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "Docker Compose is not installed. Please install Docker Compose before continuing."
    exit 1
fi

# Start PostgreSQL
echo "Starting PostgreSQL with Docker..."
cd "$(dirname "$0")" || exit
$DOCKER_COMPOSE_CMD up -d

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
sleep 10

# Get container name
POSTGRES_CONTAINER=$($DOCKER_COMPOSE_CMD ps -q postgres 2>/dev/null)
if [ -z "$POSTGRES_CONTAINER" ]; then
    echo "Cannot find PostgreSQL container. Please check your Docker setup."
    exit 1
fi

# Check connection to PostgreSQL - safer approach
echo "Checking connection to PostgreSQL..."
MAX_RETRIES=5
RETRIES=0
CONNECTED=false

while [ $RETRIES -lt $MAX_RETRIES ]; do
    if docker exec $POSTGRES_CONTAINER pg_isready -U dbt_user -d dbt_db &> /dev/null; then
        CONNECTED=true
        break
    fi
    echo "Waiting for PostgreSQL to start (attempt $((RETRIES+1))/$MAX_RETRIES)..."
    RETRIES=$((RETRIES+1))
    sleep 5
done

if [ "$CONNECTED" = true ]; then
    echo "PostgreSQL is ready!"
else
    echo "Cannot connect to PostgreSQL after multiple attempts. Please check your Docker setup."
    exit 1
fi

# Check python/pip
PIP_CMD=""
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "pip not found. Please install Python and pip before continuing."
    exit 1
fi

# Check dbt
if ! command -v dbt &> /dev/null; then
    echo "dbt is not installed. Do you want to install dbt-postgres? (y/n)"
    read -r answer
    if [ "$answer" != "${answer#[Yy]}" ]; then
        echo "Installing dbt-postgres..."
        $PIP_CMD install dbt-postgres
        
        # Add Python path to PATH
        PYTHON_BIN_PATH="$HOME/Library/Python/3.9/bin"
        echo "Adding $PYTHON_BIN_PATH to PATH..."
        export PATH="$PATH:$PYTHON_BIN_PATH"
        
        # Check again after installation and PATH update
        if ! command -v dbt &> /dev/null; then
            echo "Cannot find dbt after installation. Will try to run directly from path."
            DBT_PATH="$PYTHON_BIN_PATH/dbt"
            if [ -f "$DBT_PATH" ]; then
                echo "Found dbt at $DBT_PATH. Will use this path."
                alias dbt="$DBT_PATH"
            else
                echo "Cannot find dbt. Please install manually: $PIP_CMD install dbt-postgres"
                exit 1
            fi
        fi
    else
        echo "Please install dbt-postgres manually ($PIP_CMD install dbt-postgres) and run the script again."
        exit 1
    fi
else
    echo "dbt is already installed."
fi

# Copy profiles.yml
echo "Copying profiles.yml..."
mkdir -p ~/.dbt
cp profiles.yml ~/.dbt/

# Change to dbt directory
echo "Changing to dbt directory..."
cd ecommerce_dbt || exit

# Ensure dbt can run by using full path if needed
DBT_CMD="dbt"
if ! command -v dbt &> /dev/null; then
    DBT_CMD="$HOME/Library/Python/3.9/bin/dbt"
    if [ ! -f "$DBT_CMD" ]; then
        echo "Cannot find dbt. Please check your installation."
        exit 1
    fi
    echo "Using full path for dbt: $DBT_CMD"
fi

# Run dbt models
echo "Running dbt models..."
$DBT_CMD run || {
    echo "Error running dbt run. Please check your dbt installation and database connection."
    exit 1
}

# Test models
echo "Testing dbt models..."
$DBT_CMD test || echo "Warning: Some tests failed. Check the report for details."

# Generate documentation
echo "Generating dbt documentation..."
$DBT_CMD docs generate || echo "Warning: Could not generate documentation. You can still use the models."

echo ""
echo "==== Setup Complete ===="
echo "To view dbt documentation, run: cd ecommerce_dbt && $DBT_CMD docs serve"
echo "To connect directly to PostgreSQL, run: psql -h localhost -U dbt_user -d dbt_db (password: dbt_password)"

# Automatically run dbt docs serve
echo ""
echo "Starting dbt documentation server..."
echo "You can view the documentation at http://localhost:8080"
echo "Press Ctrl+C to stop the server when finished."
$DBT_CMD docs serve 