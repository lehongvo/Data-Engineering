#!/bin/bash

echo "==== dbt Data Mart Exercise ===="

# Add Python user bin path to PATH
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

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

# Check dbt
if ! command -v dbt &> /dev/null; then
    echo "dbt not found. Please install dbt-postgres before continuing."
    exit 1
else
    echo "dbt is installed at $(which dbt)"
fi

# Function to log information
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1"
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1" >> logs/run_$(date '+%Y%m%d').log
}

# Function to log errors
log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1" >&2
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1" >> logs/run_$(date '+%Y%m%d').log
}

# Create logs directory
mkdir -p logs

log_info "Starting PostgreSQL with Docker..."
cd "$(dirname "$0")" || exit
$DOCKER_COMPOSE_CMD up -d

# Wait for PostgreSQL to start
log_info "Waiting for PostgreSQL to start..."
sleep 10

# Copy profiles.yml
log_info "Copying profiles.yml..."
mkdir -p ~/.dbt
cp profiles.yml ~/.dbt/

# Change to dbt directory
log_info "Changing to dbt directory..."
cd ecommerce_dbt || exit

# Install dbt packages
log_info "Installing dbt packages..."
dbt deps || {
    log_error "Error installing dbt packages. Please check your dbt installation."
    exit 1
}

# Run dbt debug
log_info "Testing dbt connection..."
dbt debug || {
    log_error "Error testing dbt connection. Please check your dbt installation and database connection."
    exit 1
}

# Run the sources, staging, and core models
log_info "Running core models..."
dbt run --select source:* staging.* core.* || {
    log_error "Error running core models. Please check your dbt models."
    exit 1
}

# Run tests on core models
log_info "Running tests on core models..."
mkdir -p ../reports
dbt test --select core.* --store-failures > ../reports/core_test_results.log 2>&1

# Run materialized views for the data mart
log_info "Building data mart dimensions..."
dbt run --select mart.dimensions.* || {
    log_error "Error building data mart dimensions. Please check your dimension models."
    exit 1
}

log_info "Building data mart facts..."
dbt run --select mart.facts.* || {
    log_error "Error building data mart facts. Please check your fact models."
    exit 1
}

log_info "Building data mart metrics..."
dbt run --select mart.metrics.* || {
    log_error "Error building data mart metrics. Please check your metric models."
    exit 1
}

# Run tests on mart models
log_info "Running tests on data mart models..."
dbt test --select mart.* --store-failures > ../reports/mart_test_results.log 2>&1

# Gather model statistics
log_info "Gathering model statistics..."
dbt compile
dbt ls --resource-type model --output json > ../reports/models_info.json

# Generate documentation
log_info "Generating dbt documentation..."
dbt docs generate || log_error "Warning: Could not generate documentation. You can still use the models."

# Create summary report
CORE_TESTS_TOTAL=$(grep -c "PASS" ../reports/core_test_results.log)
CORE_TESTS_FAILED=$(grep -c "FAIL" ../reports/core_test_results.log)
MART_TESTS_TOTAL=$(grep -c "PASS" ../reports/mart_test_results.log)
MART_TESTS_FAILED=$(grep -c "FAIL" ../reports/mart_test_results.log)
TOTAL_MODELS=$(grep -c "model" ../reports/models_info.json)

cat > ../reports/datamart_summary.md << EOL
# dbt Data Mart Report

## Summary

- Total models: $TOTAL_MODELS
- Core tests passed: $CORE_TESTS_TOTAL
- Core tests failed: $CORE_TESTS_FAILED
- Mart tests passed: $MART_TESTS_TOTAL
- Mart tests failed: $MART_TESTS_FAILED

## Model Structure

\`\`\`
Sources → Staging → Core (Star Schema) → Data Mart (Metrics)
\`\`\`

## Key Metrics Available

- Daily Sales Performance
- Monthly Sales Growth
- Customer Retention Analysis
- Product Category Performance
- Customer Segmentation
EOL

log_info "Data Mart build complete"
echo ""
echo "==== Setup Complete ===="
echo "Test results: Core ($CORE_TESTS_TOTAL passed, $CORE_TESTS_FAILED failed), Mart ($MART_TESTS_TOTAL passed, $MART_TESTS_FAILED failed)"
echo "See detailed reports in the reports/ directory"
echo "To view dbt documentation, run: cd ecommerce_dbt && dbt docs serve"
echo "To connect directly to PostgreSQL, run: psql -h localhost -U dbt_user -d dbt_db_ex3 -p 5434 (password: dbt_password)" 