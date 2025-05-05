#!/bin/bash
# Run a specific ExerciseN.py script in the Exercise directory based on user input

# Start PostgreSQL with docker-compose (if not already running)
echo "Starting PostgreSQL with docker-compose..."
docker-compose up -d

# Set the path to your PostgreSQL JDBC driver (.jar)
JDBC_JAR_PATH="/Users/user/Downloads/postgresql-42.7.5.jar"
# Set the path to GCS connector
GCS_CONNECTOR_PATH="/Users/user/Downloads/gcs-connector-hadoop3-latest.jar"

read -p "Enter exercise number to run (1-6): " ex_num

script="Exercise${ex_num}.py"

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
    else
        export PYSPARK_SUBMIT_ARGS="--jars $JDBC_JAR_PATH pyspark-shell"
        echo "Using JDBC driver: $JDBC_JAR_PATH"
    fi
    python3 "$script"
    echo "\n"
else
    echo "No script found for exercise $ex_num."
fi
