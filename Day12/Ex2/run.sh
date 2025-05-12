#!/bin/bash

echo "==== dbt Testing and Documentation Exercise ===="

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

# Start PostgreSQL
echo "Starting PostgreSQL with Docker..."
cd "$(dirname "$0")" || exit
$DOCKER_COMPOSE_CMD up -d

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
sleep 10

# Copy profiles.yml
echo "Copying profiles.yml..."
mkdir -p ~/.dbt
cp profiles.yml ~/.dbt/

# Change to dbt directory
echo "Changing to dbt directory..."
cd ecommerce_dbt || exit

# Install packages
echo "Installing dbt packages..."
dbt deps || {
    echo "Error installing dbt packages. Please check your dbt installation."
    exit 1
}

# Run dbt debug
echo "Testing dbt connection..."
dbt debug || {
    echo "Error testing dbt connection. Please check your dbt installation and database connection."
    exit 1
}

# Run dbt models
echo "Running dbt models..."
dbt run || {
    echo "Error running dbt models. Please check your dbt models."
    exit 1
}

# Run tests and capture results
echo "Running tests..."
mkdir -p ../reports
dbt test --store-failures > ../reports/test_results.log 2>&1

# Check number of tests passed
TESTS_TOTAL=$(grep -c "PASS" ../reports/test_results.log)
TESTS_FAILED=$(grep -c "FAIL" ../reports/test_results.log)

# Create summary report
cat > ../reports/test_summary.md << EOL
# dbt Test Report

## Summary

- Total tests run: $((TESTS_TOTAL + TESTS_FAILED))
- Tests passed: $TESTS_TOTAL
- Tests failed: $TESTS_FAILED

## Details

$(grep -n "PASS\|FAIL" ../reports/test_results.log | sed 's/^/- /')

## Detailed Errors

\`\`\`
$(grep -A 10 -B 2 "FAIL" ../reports/test_results.log)
\`\`\`
EOL

# Generate documentation
echo "Generating dbt documentation..."
dbt docs generate || echo "Warning: Could not generate documentation. You can still use the models."

echo ""
echo "==== Setup Complete ===="
echo "Test results: $TESTS_TOTAL passed, $TESTS_FAILED failed"
echo "See detailed reports in the reports/ directory"
echo "To view dbt documentation, run: cd ecommerce_dbt && dbt docs serve"
echo "To connect directly to PostgreSQL, run: psql -h localhost -U dbt_user -d dbt_db_ex2 -p 5433 (password: dbt_password)" 
 