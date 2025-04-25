from google.cloud import storage, bigquery
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import os

# Configuration
PROJECT_ID = "unique-axle-457602-n6"
BUCKET_NAME = "data-engineering-practice-data-lake-dev"
DATASET_ID = "data_engineering_practice_dev"
TABLE_ID = "raw_sales_data"

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "../../***REMOVED***"
)


def generate_sample_data(num_records=2000):
    """Generate sample sales data"""
    print("Generating sample data...")

    # Generate random dates for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = [
        start_date
        + timedelta(
            days=np.random.randint(0, 31),
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )
        for _ in range(num_records)
    ]

    data = {
        "transaction_id": [str(uuid.uuid4()) for _ in range(num_records)],
        "customer_id": [
            f"CUST_{np.random.randint(1, 101):03d}" for _ in range(num_records)
        ],
        "amount": np.random.uniform(10.0, 1000.0, num_records).round(2),
        "transaction_date": dates,
    }

    return pd.DataFrame(data)


def upload_to_gcs(df, bucket_name, blob_name):
    """Upload DataFrame to Google Cloud Storage"""
    print(f"Uploading to Cloud Storage bucket: {bucket_name}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Save DataFrame to CSV in memory and upload
    blob.upload_from_string(df.to_csv(index=False), "text/csv")
    print(f"File uploaded to: gs://{bucket_name}/{blob_name}")


def get_bigquery_schema(df):
    """Convert pandas DataFrame schema to BigQuery schema"""
    type_mapping = {
        "object": "STRING",
        "int64": "INTEGER",
        "float64": "FLOAT",
        "datetime64[ns]": "TIMESTAMP",
        "bool": "BOOLEAN",
    }

    schema = []
    for column, dtype in df.dtypes.items():
        bq_type = type_mapping.get(str(dtype), "STRING")
        schema.append(bigquery.SchemaField(column, bq_type, mode="REQUIRED"))
    return schema


def load_to_bigquery(bucket_name, blob_name, dataset_id, table_id, df):
    """Load data from GCS to BigQuery"""
    print(f"Loading data to BigQuery table: {dataset_id}.{table_id}")

    client = bigquery.Client()
    table_ref = f"{PROJECT_ID}.{dataset_id}.{table_id}"

    # Get schema from DataFrame
    schema = get_bigquery_schema(df)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=schema,
    )

    uri = f"gs://{bucket_name}/{blob_name}"
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()  # Wait for the job to complete

    # Get table info and print row count
    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows into {table_ref}")


def main():
    try:
        # Generate sample data
        df = generate_sample_data()
        print(f"Generated {len(df)} records")

        # Upload to Cloud Storage
        blob_name = f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        upload_to_gcs(df, BUCKET_NAME, blob_name)

        # Print Cloud Storage link
        gcs_link = f"https://console.cloud.google.com/storage/browser/{BUCKET_NAME}/{blob_name}"
        print(f"\nCloud Storage Link:")
        print(f"🔗 {gcs_link}")

        # Load to BigQuery with DataFrame schema
        load_to_bigquery(BUCKET_NAME, blob_name, DATASET_ID, TABLE_ID, df)

        # Print BigQuery link
        bq_link = f"https://console.cloud.google.com/bigquery?project={PROJECT_ID}&p={PROJECT_ID}&d={DATASET_ID}&t={TABLE_ID}&page=table"
        print(f"\nBigQuery Table Link:")
        print(f"🔗 {bq_link}")

        print("\nData pipeline completed successfully! 🎉")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()
