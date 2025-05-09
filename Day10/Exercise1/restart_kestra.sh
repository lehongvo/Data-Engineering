#!/bin/bash

echo "Restarting Kestra container..."
docker-compose restart kestra

echo "Waiting for Kestra to start (30 seconds)..."
sleep 30

echo "Creating necessary directories in container..."
docker exec -it kestra mkdir -p /app/flows
docker exec -it kestra mkdir -p /app/storage

echo "Copying flow files to container..."
docker cp flows/kafka_consume_example.yml kestra:/app/flows/
docker cp flows/kafka_produce_example.yml kestra:/app/flows/

echo "Checking Kestra API health..."
curl -s --head --request GET http://localhost:8090/api/v1/health | grep HTTP

echo "Checking available flows..."
curl -s http://localhost:8090/api/v1/flows/search | grep -i kafka

echo "Done! You can now access Kestra UI at http://localhost:8090" 