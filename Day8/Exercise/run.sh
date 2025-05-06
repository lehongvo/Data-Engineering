#!/bin/bash
# Run a specific ExerciseN.py script in the Exercise directory based on user input

# Start PostgreSQL with docker-compose (if not already running)
echo "Starting PostgreSQL, Kafka, and Zookeeper with docker-compose..."
docker-compose up -d

# Set the path to your PostgreSQL JDBC driver (.jar)
JDBC_JAR_PATH="/Users/user/Downloads/postgresql-42.7.5.jar"
# Set the path to GCS connector
GCS_CONNECTOR_PATH="/Users/user/Downloads/gcs-connector-hadoop3-latest.jar"

read -p "Enter exercise number to run (1-6): " ex_num

script="Exercise${ex_num}.py"

wait_for_kafka() {
    echo "Checking if Kafka broker is ready on localhost:9092..."
    for i in {1..15}; do
        if nc -z localhost 9092; then
            echo "Kafka broker is up!"
            return 0
        fi
        echo "Waiting for Kafka to be ready... ($i/15)"
        sleep 2
    done
    echo "ERROR: Kafka broker is not available on localhost:9092. Please check your docker-compose setup."
    exit 1
}

if [ -f "$script" ]; then
    echo "==============================="
    echo "Running $script"
    echo "==============================="
    if [ "$ex_num" = "4" ]; then
        # Set Google credentials for BigQuery
        export GOOGLE_APPLICATION_CREDENTIALS="/Users/user/Desktop/Data-Engineering/Day8/config/service-account.json"
        echo "Using Google credentials: $GOOGLE_APPLICATION_CREDENTIALS"
        
        # Set Hadoop configurations directly
        export PYSPARK_SUBMIT_ARGS="--conf spark.hadoop.google.cloud.auth.service.account.enable=true \
        --conf spark.hadoop.google.cloud.auth.service.account.json.keyfile=$GOOGLE_APPLICATION_CREDENTIALS \
        --conf spark.hadoop.fs.gs.impl=com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem \
        --conf spark.hadoop.fs.AbstractFileSystem.gs.impl=com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS \
        --conf spark.hadoop.fs.gs.project.id=unique-axle-457602-n6 \
        --jars $JDBC_JAR_PATH,$GCS_CONNECTOR_PATH \
        --packages com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.36.1 \
        pyspark-shell"
        
        echo "Using JDBC driver, GCS connector, and BigQuery connector with full configuration"
    elif [ "$ex_num" = "5" ]; then
        echo "Checking and installing required Python packages for Exercise 5..."
        if [ ! -d ".venv" ]; then
            echo "Creating Python virtual environment for Exercise 5..."
            python3 -m venv .venv
        fi
        source .venv/bin/activate
        pip install pyspark kafka-python elasticsearch
        export PYSPARK_SUBMIT_ARGS="--jars $JDBC_JAR_PATH --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 pyspark-shell"
        echo "Using JDBC driver: $JDBC_JAR_PATH"
        wait_for_kafka
    else
        export PYSPARK_SUBMIT_ARGS="--jars $JDBC_JAR_PATH pyspark-shell"
        echo "Using JDBC driver: $JDBC_JAR_PATH"
    fi
    python3 "$script"
    if [ "$ex_num" = "5" ]; then
        deactivate
    fi
    echo "\n"
else
    echo "No script found for exercise $ex_num."
fi
