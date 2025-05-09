"""
Example of how to connect data from Flink to BigQuery
In actual production, you'll need to use the official Flink Connector for BigQuery
"""
from google.cloud import bigquery
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

class BigQueryWriter:
    """
    Class for writing data from Flink to BigQuery
    """
    def __init__(self, project_id=None, dataset_id=None, table_id=None, credentials_path=None):
        """
        Initialize BigQuery connection
        """
        # Use provided account key
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        else:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './config/account_key.json'
        
        # Use project ID from account key if not provided
        self.project_id = project_id or "unique-axle-457602-n6"
        self.dataset_id = dataset_id or "clickstream_analytics"
        self.table_id = table_id or "user_page_stats"
        self.full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        
        try:
            self.client = bigquery.Client()
            print(f"Successfully connected to BigQuery project {self.project_id}")
        except Exception as e:
            print(f"Error connecting to BigQuery: {e}")
            sys.exit(1)
        
        self._validate_table()
    
    def _validate_table(self):
        """
        Check if table exists, create it if it doesn't
        """
        try:
            self.client.get_table(self.full_table_id)
            print(f"Table {self.full_table_id} already exists")
        except Exception:
            print(f"Table {self.full_table_id} doesn't exist, creating it...")
            schema = [
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("page", "STRING"),
                bigquery.SchemaField("view_count", "INTEGER"),
                bigquery.SchemaField("avg_session_duration", "FLOAT"),
                bigquery.SchemaField("last_activity", "STRING")
            ]
            table = bigquery.Table(self.full_table_id, schema=schema)
            self.client.create_table(table)
            print(f"Created table {self.full_table_id}")
    
    def insert_rows(self, rows):
        """
        Write data to BigQuery
        """
        errors = self.client.insert_rows_json(self.full_table_id, rows)
        if errors:
            print(f"Error inserting data: {errors}")
            return False
        return True

def process_from_kafka_to_bigquery(kafka_data, bq_writer):
    """
    Process data from Kafka then write to BigQuery
    """
    # Parse data from Kafka (assuming JSON)
    try:
        data = json.loads(kafka_data)
        
        # Process data (in reality would use Flink)
        processed_data = {
            "user_id": data.get("user_id"),
            "page": data.get("page"),
            "view_count": 1,  # In reality would be more complex calculation
            "avg_session_duration": data.get("session_duration", 0),
            "last_activity": data.get("timestamp")
        }
        
        # Write to BigQuery
        bq_writer.insert_rows([processed_data])
        print(f"Processed and wrote data: {processed_data}")
        
    except json.JSONDecodeError:
        print(f"Invalid data: {kafka_data}")
    except Exception as e:
        print(f"Error processing data: {e}")

def demo_pipeline():
    """
    Demo pipeline Kafka -> Process -> BigQuery
    """
    # Set up BigQuery connection with provided account
    bq_writer = BigQueryWriter(
        project_id="unique-axle-457602-n6",
        dataset_id="clickstream_analytics",
        table_id="user_page_stats",
        credentials_path="./config/account_key.json"
    )
    
    # Simulate data from Kafka
    sample_data = [
        '{"event_id": "e1", "user_id": "user1", "page": "/home", "action": "view", "device": "mobile", "timestamp": "2023-01-01T12:00:00", "session_duration": 120}',
        '{"event_id": "e2", "user_id": "user2", "page": "/products", "action": "click", "device": "desktop", "timestamp": "2023-01-01T12:01:00", "session_duration": 45}',
        '{"event_id": "e3", "user_id": "user1", "page": "/cart", "action": "click", "device": "mobile", "timestamp": "2023-01-01T12:02:00", "session_duration": 75}'
    ]
    
    # Process in parallel with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        for data in sample_data:
            executor.submit(process_from_kafka_to_bigquery, data, bq_writer)
            time.sleep(1)  # Simulate delay

if __name__ == "__main__":
    print("Demo BigQuery connection")
    demo_pipeline() 