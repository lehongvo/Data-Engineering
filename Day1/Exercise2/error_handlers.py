from flask import jsonify
from functools import wraps
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BigQueryError(Exception):
    """Custom exception for BigQuery related errors"""

    def __init__(self, message="BigQuery operation failed", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def handle_bigquery_error(error):
    """Handler for BigQuery errors"""
    logger.error(f"BigQuery error: {str(error)}")
    response = {"status": "error", "message": str(error), "error_type": "BigQueryError"}
    return jsonify(response), getattr(error, "status_code", 500)


def error_handler(f):
    """Decorator for handling errors in routes"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BigQueryError as e:
            return handle_bigquery_error(e)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "An unexpected error occurred",
                        "error_type": "UnexpectedError",
                    }
                ),
                500,
            )

    return decorated_function
