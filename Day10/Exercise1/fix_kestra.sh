#!/bin/bash

echo "====== Attempting to fix Kestra flows ======"

echo "1. Stopping and removing Kestra container..."
docker-compose stop kestra
docker-compose rm -f kestra

echo "2. Removing any leftover data..."
rm -rf data/kestra

echo "3. Setting up necessary directories..."
mkdir -p data/kestra/storage
mkdir -p data/kestra/plugins

echo "4. Updating volume paths in docker-compose file..."
# This is just informational - we'll use the existing paths

echo "5. Starting Kestra with proper configuration..."
docker-compose up -d kestra

echo "6. Waiting for Kestra to start (30 seconds)..."
sleep 30

echo "7. Directly uploading flows via API..."
curl -v -X POST "http://localhost:8090/api/v1/flows" -H "Content-Type: application/yaml" --data-binary @flows/hello_world.yml
echo ""
echo "8. Checking flows on API..."
curl -s "http://localhost:8090/api/v1/flows/search" | grep -i hello
echo ""

echo "9. Attempting to directly access files in container..."
docker exec -it kestra ls -la /app/flows/

echo "10. Copying files directly to container..."
docker cp flows/hello_world.yml kestra:/app/flows/
docker cp src/kestra/flows/hello_world.yml kestra:/app/flows/hello_world_2.yml

echo "11. Checking if files were copied successfully..."
docker exec -it kestra ls -la /app/flows/

echo "12. Restarting Kestra to reload flows..."
docker-compose restart kestra
sleep 15

echo "13. Final check for flows..."
curl -s "http://localhost:8090/api/v1/flows/search" | grep -i hello

echo "====== Completed troubleshooting steps ======"
echo "If flows are still not showing, check Kestra logs with: docker logs kestra"
echo "You can access Kestra UI at: http://localhost:8090" 