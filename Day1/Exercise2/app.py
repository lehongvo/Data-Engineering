from flask import Flask, render_template, jsonify, request
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core import retry
import os
from dotenv import load_dotenv
from error_handlers import error_handler, BigQueryError
import logging
from rate_limiter import rate_limit
from datetime import datetime
import math

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get API key from environment
API_KEY_INSERT = os.getenv("API_KEY_INSERT")
if not API_KEY_INSERT:
    logger.warning("API_KEY_INSERT not set in environment variables")

# Constants
RECORDS_PER_PAGE = 10


def validate_api_key(api_key):
    """Validate the API key"""
    return api_key == API_KEY_INSERT


def get_bigquery_client():
    """
    Creates and returns a BigQuery client using credentials from environment variables
    """
    try:
        # Check if using service account key file
        key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.getenv("GCP_PROJECT_ID")

        if not project_id:
            raise BigQueryError("GCP_PROJECT_ID environment variable is not set", 500)

        if key_path and os.path.exists(key_path):
            # Using service account key file
            credentials = service_account.Credentials.from_service_account_file(
                key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            client = bigquery.Client(credentials=credentials, project=project_id)
        else:
            # Using application default credentials or metadata server on GCP
            client = bigquery.Client(project=project_id)

        logger.info(f"BigQuery client created successfully for project: {project_id}")
        return client
    except Exception as e:
        logger.error(f"Failed to create BigQuery client: {str(e)}")
        raise BigQueryError(f"Failed to create BigQuery client: {str(e)}", 500)


@app.route("/")
def home():
    """Home page with simple welcome message"""
    return render_template("index.html")


@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route("/test", methods=["GET"])
@rate_limit()  # Default: 100 requests per minute
@error_handler
def test_bigquery():
    """
    Test BigQuery connection by running a query on test_table
    """
    try:
        client = get_bigquery_client()
        query = """
            SELECT 'Connection Successful' as status
        """
        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            return jsonify({"status": "success", "message": row.status})
    except Exception as e:
        logger.error(f"Error in test_bigquery: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/records", methods=["GET"])
@rate_limit()  # Default: 100 requests per minute
@error_handler
def get_records():
    """
    Get records from test_table with optional filters and pagination
    """
    try:
        # Get query parameters
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))  # Default 10 items per page
        name_filter = request.args.get("name")
        min_age = request.args.get("min_age")
        max_age = request.args.get("max_age")

        # Validate and limit per_page parameter
        per_page = min(max(per_page, 5), 50)  # Limit between 5 and 50 items

        # Get BigQuery client and project ID
        client = get_bigquery_client()
        project_id = client.project

        # Build WHERE clause based on filters
        where_clauses = []
        if name_filter:
            where_clauses.append(f"LOWER(full_name) LIKE LOWER('%{name_filter}%')")
        if min_age:
            where_clauses.append(f"age >= {int(min_age)}")
        if max_age:
            where_clauses.append(f"age <= {int(max_age)}")

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        # Count total records
        count_query = f"""
            SELECT COUNT(*) as total
            FROM `{project_id}.test_dataset.test_table`
            {where_sql}
        """

        # Execute count query
        count_job = client.query(count_query)
        total_records = next(count_job.result())["total"]

        # Calculate pagination
        total_pages = math.ceil(total_records / per_page)
        offset = (page - 1) * per_page

        # Get records for current page
        records_query = f"""
            SELECT 
                full_name,
                age,
                CURRENT_TIMESTAMP() as added_at
            FROM `{project_id}.test_dataset.test_table`
            {where_sql}
            ORDER BY full_name
            LIMIT {per_page}
            OFFSET {offset}
        """

        # Execute records query
        records_job = client.query(records_query)
        records = []

        for row in records_job:
            records.append(
                {
                    "full_name": row.full_name,
                    "age": row.age,
                    "added_at": row.added_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        # Prepare response
        response_data = {
            "status": "success",
            "records": records,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "per_page": per_page,
                "total_records": total_records,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
            "filters": {"name": name_filter, "min_age": min_age, "max_age": max_age},
        }

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error fetching records: {str(e)}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Failed to fetch records",
                    "error": str(e),
                }
            ),
            500,
        )


@app.route("/insert", methods=["POST"])
@rate_limit()  # Default: 100 requests per minute
def insert_record():
    """
    Insert a new record into test_table
    """
    try:
        data = request.get_json()

        # Check API key from request data
        if not data or "api_key" not in data:
            return jsonify({"status": "error", "message": "API key is required"}), 401

        if not validate_api_key(data["api_key"]):
            return jsonify({"status": "error", "message": "Invalid API key"}), 401

        # Validate required fields
        if "full_name" not in data or "age" not in data:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Missing required fields: full_name and age",
                    }
                ),
                400,
            )

        # Validate data types and values
        if not isinstance(data["full_name"], str) or not data["full_name"].strip():
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "full_name must be a non-empty string",
                    }
                ),
                400,
            )

        if not isinstance(data["age"], int) or data["age"] < 0:
            return (
                jsonify(
                    {"status": "error", "message": "age must be a non-negative integer"}
                ),
                400,
            )

        # Prepare the row to be inserted
        row = {"full_name": data["full_name"], "age": data["age"]}

        # Define table reference
        client = get_bigquery_client()
        table_ref = client.dataset("test_dataset").table("test_table")

        # Insert the row into BigQuery
        errors = client.insert_rows_json(table_ref, [row])

        if errors:
            logger.error(f"Errors inserting row: {errors}")
            return (
                jsonify(
                    {"status": "error", "message": f"Failed to insert record: {errors}"}
                ),
                500,
            )

        logger.info(f"Successfully inserted record for {data['full_name']}")
        return jsonify({"status": "success", "message": "Record inserted successfully"})

    except Exception as e:
        logger.error(f"Error in insert_record: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(host="0.0.0.0", port=port, debug=debug)
