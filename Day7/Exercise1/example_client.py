#!/usr/bin/env python3
"""
Example client for BigQuery API.

This script demonstrates how to use the BigQuery API endpoints.
"""

import requests
import json
import os
import sys

# API server URL
API_URL = "http://localhost:8000"
# API Key for authentication
API_KEY = "u28c9872hc7h384g3784hcb34vuvfh34897hj3489"
# Headers to include in all requests
API_HEADERS = {"X-API-Key": API_KEY}


def import_csv(file_path):
    """
    Import a CSV file to BigQuery.

    Args:
        file_path: Path to CSV file

    Returns:
        Response from API
    """
    url = f"{API_URL}/import-csv/"

    # Ensure file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return None

    # Get filename for display
    filename = os.path.basename(file_path)

    print(f"Importing {filename} to BigQuery...")

    # Create multipart form with file
    files = {"file": (filename, open(file_path, "rb"), "text/csv")}

    # Send request with API key
    response = requests.post(url, files=files, headers=API_HEADERS)

    # Check response
    if response.status_code == 200:
        result = response.json()
        print(
            f"Success! Imported {result['rows_imported']} rows into {result['table_id']}"
        )
        print(f"Schema: {len(result['schema'])} fields detected")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def get_data(table_id, limit=10):
    """
    Get data from a table.

    Args:
        table_id: Table ID
        limit: Maximum number of rows to return

    Returns:
        Response from API
    """
    url = f"{API_URL}/data/{table_id}"

    if limit:
        url += f"?limit={limit}"

    print(f"Getting data from {table_id} (limit: {limit})...")

    # Send request with API key
    response = requests.get(url, headers=API_HEADERS)

    # Check response
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Got {result['rows']} rows of data")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def get_schema(table_id):
    """
    Get schema of a table.

    Args:
        table_id: Table ID

    Returns:
        Response from API
    """
    url = f"{API_URL}/schema/{table_id}"

    print(f"Getting schema for {table_id}...")

    # Send request with API key
    response = requests.get(url, headers=API_HEADERS)

    # Check response
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Schema has {len(result['schema'])} fields")
        for field in result["schema"]:
            print(f"  - {field['name']}: {field['type']} ({field['mode']})")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def run_query(query):
    """
    Run a custom SQL query.

    Args:
        query: SQL query string

    Returns:
        Response from API
    """
    url = f"{API_URL}/run-query/"

    print(f"Running query: {query[:50]}...")

    # Send request with JSON body and API key
    response = requests.post(url, json={"query": query}, headers=API_HEADERS)

    # Check response
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Query returned {result['rows']} rows")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def check_health():
    """
    Check API health.

    Returns:
        Response from API
    """
    url = f"{API_URL}/health"

    print("Checking API health...")

    # Send request with API key
    response = requests.get(url, headers=API_HEADERS)

    # Check response
    if response.status_code == 200:
        result = response.json()
        print(f"API is {result['status']}, version {result['version']}")
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def main():
    """Main entry point."""

    if len(sys.argv) < 2:
        print("Usage: python example_client.py COMMAND [ARGS]")
        print("Commands:")
        print("  import CSV_FILE")
        print("  data TABLE_ID [LIMIT]")
        print("  schema TABLE_ID")
        print("  query SQL_QUERY")
        print("  health")
        return

    command = sys.argv[1].lower()

    if command == "import" and len(sys.argv) >= 3:
        import_csv(sys.argv[2])
    elif command == "data" and len(sys.argv) >= 3:
        limit = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
        get_data(sys.argv[2], limit)
    elif command == "schema" and len(sys.argv) >= 3:
        get_schema(sys.argv[2])
    elif command == "query" and len(sys.argv) >= 3:
        run_query(" ".join(sys.argv[2:]))
    elif command == "health":
        check_health()
    else:
        print("Unknown command or missing arguments")


if __name__ == "__main__":
    main()
