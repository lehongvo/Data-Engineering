from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form, Body, Header, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from typing import Optional
import tempfile
import os
import logging

from .bigquery_service import BigQueryService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key configuration - hardcoded for this example
API_KEY = "u28c9872hc7h384g3784hcb34vuvfh34897hj3489"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="BigQuery API",
    description="API for importing and querying data from BigQuery",
    version="1.0.0",
)

# API Key dependency
async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key",
        )
    return api_key

# Initialize BigQuery service as a dependency
def get_bigquery_service():
    """Dependency to get BigQuery service instance."""
    try:
        return BigQueryService()
    except Exception as e:
        logger.error(f"Failed to initialize BigQuery service: {e}")
        raise HTTPException(
            status_code=500, detail=f"Service initialization error: {e}"
        )


@app.post("/import-csv/")
async def import_csv(
    api_key: str = Depends(verify_api_key),
    file: UploadFile = File(...),
    bq_service: BigQueryService = Depends(get_bigquery_service),
):
    """
    Import CSV file to BigQuery.

    - **file**: CSV file to import

    Returns import summary including schema and row count.
    """
    try:
        logger.info(f"Received file: {file.filename}")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            logger.info(f"Saved temporary file to: {temp_path}")

        # Get table name from file name
        file_name = os.path.splitext(file.filename)[0]
        table_id = f"{file_name}_data"
        logger.info(f"Table ID: {table_id}")

        # Import CSV
        result = await bq_service.import_csv(temp_path, table_id)

        # Clean up
        os.unlink(temp_path)
        logger.info(f"Import completed successfully")

        return result
    except Exception as e:
        logger.error(f"Error importing CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{table_id}")
async def get_data(
    table_id: str,
    limit: Optional[int] = None,
    api_key: str = Depends(verify_api_key),
    bq_service: BigQueryService = Depends(get_bigquery_service),
):
    """
    Get data from specified table.

    - **table_id**: Name of the table
    - **limit**: Optional row limit

    Returns table data as JSON.
    """
    try:
        return await bq_service.get_data(table_id, limit)
    except Exception as e:
        logger.error(f"Error getting data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schema/{table_id}")
async def get_schema(
    table_id: str, 
    api_key: str = Depends(verify_api_key),
    bq_service: BigQueryService = Depends(get_bigquery_service)
):
    """
    Get schema of specified table.

    - **table_id**: Name of the table

    Returns table schema information.
    """
    try:
        return await bq_service.get_schema(table_id)
    except Exception as e:
        logger.error(f"Error getting schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run-query/")
async def run_query(
    query_data: dict = Body(...),
    api_key: str = Depends(verify_api_key),
    bq_service: BigQueryService = Depends(get_bigquery_service),
):
    """
    Run a custom SQL query.

    - **query**: SQL query string

    Returns query results as JSON.
    """
    try:
        if "query" not in query_data:
            raise HTTPException(status_code=400, detail="Query parameter is required")

        query = query_data["query"]
        logger.info(f"Running query: {query[:50]}...")

        return await bq_service.run_query(query)
    except Exception as e:
        logger.error(f"Error running query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check(api_key: str = Depends(verify_api_key)):
    """
    Check API health.

    Returns status and version information.
    """
    return {"status": "healthy", "version": app.version, "title": app.title}
