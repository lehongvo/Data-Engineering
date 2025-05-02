from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os
from typing import Optional, List, Dict, Any, Union
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BigQueryService:
    def __init__(self, key_path=None):
        """Initialize BigQuery client with service account credentials."""
        try:
            # Path to service account key file
            if key_path is None:
                key_path = os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "config",
                    "cgp-service-account-key.json",
                )

            if not os.path.exists(key_path):
                raise Exception(f"Service account key file not found at {key_path}")

            # Create credentials from service account key
            credentials = service_account.Credentials.from_service_account_file(
                key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )

            # Initialize client with credentials
            self.client = bigquery.Client(
                credentials=credentials, project=credentials.project_id
            )
            self.dataset_id = "exercise1"
            self.project_id = credentials.project_id

            logger.info(f"BigQuery client initialized for project: {self.project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery client: {e}")
            raise

    def get_full_table_id(self, table_id: str) -> str:
        """Get fully qualified table ID."""
        return f"{self.project_id}.{self.dataset_id}.{table_id}"

    async def import_csv(self, file_path: str, table_id: str = None) -> Dict[str, Any]:
        """
        Import CSV file to BigQuery with auto-detected schema.

        Args:
            file_path: Path to CSV file
            table_id: Optional table ID, if None will be derived from file name

        Returns:
            Dict with import summary
        """
        try:
            # Get table name from file name if not provided
            if table_id is None:
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                table_id = f"{file_name}_data"

            # Configure load job
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,
                autodetect=True,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            )

            # Load data
            with open(file_path, "rb") as f:
                load_job = self.client.load_table_from_file(
                    f, self.get_full_table_id(table_id), job_config=job_config
                )

            load_job.result()  # Wait for job

            # Get table info
            table = self.client.get_table(self.get_full_table_id(table_id))

            # Return import summary
            schema_info = [
                {"name": field.name, "type": field.field_type} for field in table.schema
            ]

            return {
                "status": "success",
                "table_id": table_id,
                "rows_imported": table.num_rows,
                "schema": schema_info,
            }

        except Exception as e:
            logger.error(f"Failed to import CSV {file_path}: {e}")
            raise

    async def get_data(
        self, table_id: str, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get data from specified table."""
        try:
            query = f"SELECT * FROM `{self.get_full_table_id(table_id)}`"
            if limit:
                query += f" LIMIT {limit}"

            query_job = self.client.query(query)
            results = query_job.result()
            df = results.to_dataframe()

            return {
                "status": "success",
                "rows": len(df),
                "data": df.to_dict(orient="records"),
            }

        except Exception as e:
            logger.error(f"Failed to get data from {table_id}: {e}")
            raise

    async def get_schema(self, table_id: str) -> Dict[str, Any]:
        """Get schema of specified table."""
        try:
            table = self.client.get_table(self.get_full_table_id(table_id))
            schema_info = [
                {
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description,
                }
                for field in table.schema
            ]

            return {"status": "success", "table_id": table_id, "schema": schema_info}

        except Exception as e:
            logger.error(f"Failed to get schema for {table_id}: {e}")
            raise

    async def run_query(self, query: str) -> Dict[str, Any]:
        """
        Run a custom SQL query.

        Args:
            query: SQL query string

        Returns:
            Dict with query results
        """
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            df = results.to_dataframe()

            return {
                "status": "success",
                "rows": len(df),
                "data": df.to_dict(orient="records"),
            }

        except Exception as e:
            logger.error(f"Failed to run query: {e}")
            raise

    async def setup_dataset(self) -> Dict[str, Any]:
        """
        Setup dataset - create if not exists.

        Returns:
            Dict with status
        """
        try:
            # Check if dataset exists
            try:
                self.client.get_dataset(self.dataset_id)
                logger.info(f"Dataset {self.dataset_id} already exists")
                dataset_exists = True
            except Exception:
                dataset_exists = False

            # Create dataset if not exists
            if not dataset_exists:
                dataset = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
                dataset.location = "US"
                self.client.create_dataset(dataset)
                logger.info(f"Created dataset {self.dataset_id}")

            return {
                "status": "success",
                "dataset_id": self.dataset_id,
                "project_id": self.project_id,
            }

        except Exception as e:
            logger.error(f"Failed to setup dataset: {e}")
            raise
