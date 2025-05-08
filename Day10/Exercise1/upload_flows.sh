#!/bin/bash

# Set working directory
cd "$(dirname "$0")"

# Kiểm tra jq đã được cài đặt chưa
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed. Please install jq first."
    exit 1
fi

echo "=== Checking Kestra API ==="
if curl -s --head --request GET http://localhost:8090/api/v1/health 2>/dev/null | grep "200" > /dev/null; then
    echo "Kestra API is working properly!"
else
    echo "WARNING: Kestra API is not responding correctly. Check if Kestra is running properly."
    echo "Trying to upload flows anyway..."
fi

# Delete all existing flows before uploading
echo "=== Deleting all existing flows ==="
# Get all namespaces
namespaces=$(curl -s "http://localhost:8090/api/v1/flows/distinct-namespaces" | jq -r '.[]')
for namespace in $namespaces; do
    echo "Checking namespace: $namespace"
    # Get all flows in the namespace
    flows=$(curl -s "http://localhost:8090/api/v1/flows/$namespace" | jq -r '.[].id')
    for flow in $flows; do
        echo "Deleting flow: $namespace/$flow"
        curl -s -X DELETE "http://localhost:8090/api/v1/flows/$namespace/$flow"
    done
done
echo "All existing flows have been deleted."

# Create flows directory if it doesn't exist
mkdir -p flows

# Copy flow files to the flows directory for easier upload
cp src/kestra/flows/*.yml flows/

# Count the number of flow files
flow_files=(flows/*.yml)
file_count=${#flow_files[@]}
echo "=== Found $file_count flow files to upload ==="

# Push all flow files to Kestra API
echo "=== Uploading flow files to Kestra ==="
counter=1
for flow_file in flows/*.yml; do
    echo "[$counter/$file_count] Uploading $flow_file..."
    response=$(curl -s -X POST "http://localhost:8090/api/v1/flows" \
        -H "Content-Type: application/yaml" \
        --data-binary @"$flow_file" 2>&1)
    
    if echo "$response" | grep -q "id"; then
        echo "✅ Successfully uploaded $flow_file"
    else
        echo "❌ Failed to upload $flow_file"
        echo "Response: $response"
        echo ""
        echo "Attempting to upload with verbose output:"
        curl -v -X POST "http://localhost:8090/api/v1/flows" \
            -H "Content-Type: application/yaml" \
            --data-binary @"$flow_file"
    fi
    counter=$((counter + 1))
done

echo "=== Process completed ==="
echo "Kestra UI available at: http://localhost:8090"

# Confirm upload by listing all flows 
echo "=== Checking uploaded flows ==="
curl -s "http://localhost:8090/api/v1/flows" | jq '.' 