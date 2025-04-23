from google.cloud import bigquery
import os
from dotenv import load_dotenv
import random
import time
import names  # pip install names
import logging
import schedule  # pip install schedule
from datetime import datetime
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s - [%(filename)s:%(lineno)d]",
    handlers=[logging.FileHandler("cron_insert.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Lists for generating more diverse data
NATIONALITIES = [
    "American",
    "British",
    "Canadian",
    "French",
    "German",
    "Italian",
    "Japanese",
    "Korean",
    "Chinese",
    "Vietnamese",
]
OCCUPATIONS = [
    "Engineer",
    "Doctor",
    "Teacher",
    "Artist",
    "Writer",
    "Developer",
    "Designer",
    "Manager",
    "Student",
    "Researcher",
]
CITIES = [
    "New York",
    "London",
    "Paris",
    "Tokyo",
    "Berlin",
    "Rome",
    "Seoul",
    "Beijing",
    "Hanoi",
    "Toronto",
]


def get_bigquery_client():
    """Creates and returns a BigQuery client"""
    try:
        key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.getenv("GCP_PROJECT_ID")

        if not project_id:
            raise Exception("GCP_PROJECT_ID environment variable is not set")

        logger.info(f"Initializing BigQuery client for project: {project_id}")
        logger.info(
            f"Using credentials from: {key_path if key_path else 'Application Default Credentials'}"
        )

        if key_path and os.path.exists(key_path):
            credentials = service_account.Credentials.from_service_account_file(
                key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            client = bigquery.Client(credentials=credentials, project=project_id)
            logger.info("Successfully created BigQuery client using service account")
        else:
            client = bigquery.Client(project=project_id)
            logger.info(
                "Successfully created BigQuery client using default credentials"
            )

        return client
    except Exception as e:
        logger.error(f"Failed to create BigQuery client: {str(e)}")
        raise


def generate_random_records(count=10):
    """Generate random records with more diverse data"""
    try:
        logger.info(f"Generating {count} random records...")
        records = []
        for i in range(count):
            record = {
                "full_name": names.get_full_name(),
                "age": random.randint(18, 80),
                "api_key": os.getenv("API_KEY_INSERT"),
            }
            records.append(record)
            logger.debug(f"Generated record {i+1}/{count}: {record}")

        logger.info(f"Successfully generated {count} random records")
        return records
    except Exception as e:
        logger.error(f"Error generating random records: {str(e)}")
        raise


def insert_records():
    """Insert random records directly into BigQuery"""
    start_time = datetime.now()
    logger.info(f"Starting batch insert at {start_time}")

    try:
        # Get BigQuery client
        client = get_bigquery_client()

        # Generate random records
        records = generate_random_records(10)

        # Define table reference
        dataset_id = "test_dataset"
        table_id = "test_table"
        table_ref = client.dataset(dataset_id).table(table_id)

        logger.info(f"Inserting {len(records)} records into {dataset_id}.{table_id}")

        # Insert records into BigQuery
        errors = client.insert_rows_json(table_ref, records)

        if not errors:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(
                f"Successfully inserted {len(records)} records in {duration:.2f} seconds"
            )
            logger.info("Sample of inserted records:")
            for i, record in enumerate(records[:3], 1):
                logger.info(f"Record {i}: {record}")
        else:
            logger.error(f"Encountered errors while inserting records: {errors}")

    except Exception as e:
        logger.error(f"Error in insert_records: {str(e)}")
        raise


def run_job():
    """Wrapper function to run the job with error handling"""
    try:
        insert_records()
    except Exception as e:
        logger.error(f"Job failed: {str(e)}")


logger.info("=" * 50)
logger.info("Starting Cron Insert Service")
logger.info("=" * 50)

# Run insert_records immediately when the script starts
run_job()

# Schedule the job to run every 10 seconds
schedule.every(10).seconds.do(run_job)
logger.info("Scheduled job to run every 10 seconds")

# Keep the script running
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
        break
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
        time.sleep(5)  # Wait 5 seconds before retrying
