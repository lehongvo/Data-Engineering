#!/usr/bin/env python3
"""
Simple monitoring script for the Kafka-Flink-BigQuery pipeline
"""
import os
import time
import json
import subprocess
from datetime import datetime

def monitor_kafka():
    """Monitor Kafka topics and messages"""
    try:
        # Get list of topics
        result = subprocess.run(
            ["docker", "exec", "e1-kafka", "kafka-topics", "--list", "--bootstrap-server", "e1-kafka:9092"],
            capture_output=True, text=True, check=True
        )
        topics = result.stdout.strip().split('\n')
        print(f"Kafka Topics: {topics}")
        
        # Check messages in clickstream topic
        result = subprocess.run(
            ["docker", "exec", "e1-kafka", "kafka-console-consumer", 
             "--bootstrap-server", "e1-kafka:9092", "--topic", "clickstream", 
             "--from-beginning", "--max-messages", "5"],
            capture_output=True, text=True, check=False
        )
        
        print(f"Sample messages from clickstream topic:")
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    data = json.loads(line)
                    print(f"  - User: {data.get('user_id')}, Page: {data.get('page')}, Time: {data.get('timestamp')}")
                except json.JSONDecodeError:
                    print(f"  - {line}")
    except subprocess.CalledProcessError as e:
        print(f"Error monitoring Kafka: {e}")

def monitor_flink():
    """Monitor Flink jobs"""
    try:
        # Check running jobs
        result = subprocess.run(
            ["docker", "exec", "flink-jobmanager", "/opt/flink/bin/flink", "list", "-a"],
            capture_output=True, text=True, check=True
        )
        print(f"Flink Jobs:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error monitoring Flink: {e}")

def main():
    """Main monitoring loop"""
    print(f"=== Pipeline Monitoring Started at {datetime.now().isoformat()} ===")
    
    # Monitor Kafka
    print("\n=== Kafka Status ===")
    monitor_kafka()
    
    # Monitor Flink
    print("\n=== Flink Status ===")
    monitor_flink()
    
    # Check container status
    print("\n=== Container Status ===")
    subprocess.run(["docker-compose", "ps"], check=False)
    
    print(f"\n=== Monitoring Complete at {datetime.now().isoformat()} ===")

if __name__ == "__main__":
    main() 