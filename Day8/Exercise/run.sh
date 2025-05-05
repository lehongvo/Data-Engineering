#!/bin/bash
# Run a specific ExerciseN.py script in the Exercise directory based on user input

# Start PostgreSQL with docker-compose (if not already running)
echo "Starting PostgreSQL with docker-compose..."
docker-compose up -d

# Set the path to your PostgreSQL JDBC driver (.jar)
JDBC_JAR_PATH="/Users/user/Downloads/postgresql-42.7.5.jar"
export PYSPARK_SUBMIT_ARGS="--jars $JDBC_JAR_PATH pyspark-shell"

echo "Using JDBC driver: $JDBC_JAR_PATH"

read -p "Enter exercise number to run (1-6): " ex_num

script="Exercise${ex_num}.py"

if [ -f "$script" ]; then
    echo "==============================="
    echo "Running $script"
    echo "==============================="
    python3 "$script"
    echo "\n"
else
    echo "No script found for exercise $ex_num."
fi
