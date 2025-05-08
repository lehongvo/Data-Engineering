#!/bin/bash
# Run a specific ExerciseN.py script in the Exercise directory based on user input

# Start PostgreSQL with docker-compose (if not already running)
echo "Starting PostgreSQL, Kafka, and Zookeeper with docker-compose..."
docker-compose up -d

# Check if driver exists, if not, provide instructions
JDBC_JAR_PATH="/Users/user/Downloads/postgresql-42.7.5.jar"
if [ ! -f "$JDBC_JAR_PATH" ]; then
    echo "PostgreSQL JDBC driver not found at: $JDBC_JAR_PATH"
    echo "Please download it from: https://jdbc.postgresql.org/download/"
    echo "Then place it at the location specified in this script or update the path."
fi

# Set the path to GCS connector
GCS_CONNECTOR_PATH="/Users/user/Downloads/gcs-connector-hadoop3-latest.jar"
if [ ! -f "$GCS_CONNECTOR_PATH" ] && [ "$ex_num" = "4" ]; then
    echo "GCS connector not found at: $GCS_CONNECTOR_PATH"
    echo "Please download it from: https://cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage"
    echo "Then place it at the location specified in this script or update the path."
fi

read -p "Enter exercise number to run (1-6): " ex_num

script="Exercise${ex_num}.py"

wait_for_kafka() {
    echo "Checking if Kafka broker is ready on localhost:9092..."
    for i in {1..5}; do
        if nc -z localhost 9092 2>/dev/null; then
            echo "Kafka broker is up!"
            return 0
        fi
        echo "Waiting for Kafka to be ready... ($i/5)"
        sleep 2
    done
    echo "WARNING: Kafka broker is not available on localhost:9092."
    read -p "Do you want to continue anyway? (y/n): " continue_anyway
    if [ "$continue_anyway" != "y" ]; then
        echo "Exiting. Please check your docker-compose setup."
        exit 1
    fi
    echo "Continuing without Kafka..."
}

if [ -f "$script" ]; then
    echo "==============================="
    echo "Running $script"
    echo "==============================="
    if [ "$ex_num" = "4" ]; then
        # Set Google credentials for BigQuery
        CREDENTIALS_PATH="/Users/user/Desktop/Data-Engineering/Day8/config/service-account.json"
        if [ ! -f "$CREDENTIALS_PATH" ]; then
            echo "Google credentials file not found at: $CREDENTIALS_PATH"
            echo "Please place your service account JSON file at this location or update the path."
            read -p "Do you want to continue anyway? (y/n): " continue_creds
            if [ "$continue_creds" != "y" ]; then
                exit 1
            fi
        fi
        export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_PATH"
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
    echo ""
else
    echo "No script found for exercise $ex_num."
fi
