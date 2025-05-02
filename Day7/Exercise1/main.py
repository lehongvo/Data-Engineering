#!/usr/bin/env python3
"""
BigQuery API - Main Entry Point

This module serves as the main entry point for the BigQuery API application.
It loads configuration, sets up logging, and starts the FastAPI server.

Author: Data Engineering Team
"""

import os
import sys
import logging
import argparse
import uvicorn
from api import app
from api.bigquery_service import BigQueryService
import asyncio
import glob

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="BigQuery API")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the server to"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable automatic reloading on code changes",
    )
    parser.add_argument(
        "--import-data",
        action="store_true",
        help="Import data from CSV files in data/ directory",
    )
    return parser.parse_args()


async def import_sample_data():
    """Import sample data from CSV files in data/ directory."""
    try:
        logger.info("Initializing BigQuery service...")
        bq_service = BigQueryService()

        # Setup dataset
        await bq_service.setup_dataset()

        # Find all CSV files
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

        if not csv_files:
            logger.warning("No CSV files found in data/ directory")
            return

        # Import each CSV file
        for csv_file in csv_files:
            logger.info(f"Importing {csv_file}...")
            result = await bq_service.import_csv(csv_file)
            logger.info(
                f"Imported {result['rows_imported']} rows into {result['table_id']}"
            )

        logger.info("Data import completed successfully")

    except Exception as e:
        logger.error(f"Error importing data: {e}")
        raise


def start_server(host="0.0.0.0", port=8000, reload=False):
    """Start the FastAPI server."""
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"API documentation: http://{host}:{port}/docs")
    uvicorn.run("api:app", host=host, port=port, reload=reload, log_level="info")


def main():
    """Main entry point."""
    args = parse_arguments()

    # Import data if requested
    if args.import_data:
        logger.info("Importing sample data...")
        asyncio.run(import_sample_data())

    # Start server
    start_server(args.host, args.port, args.reload)


if __name__ == "__main__":
    main()
