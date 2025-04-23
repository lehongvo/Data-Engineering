import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Optional, List, Dict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("etl_pipeline.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class EmployeeETL:
    """
    ETL pipeline for processing employee and department data.

    This class handles the extraction, transformation, and loading of employee data
    from a CSV source file, applies various transformations, and saves the result
    to a new CSV file.
    """

    def __init__(self, input_file: str, output_file: str):
        """
        Initialize the ETL pipeline.

        Args:
            input_file (str): Path to the input CSV file
            output_file (str): Path where the output CSV will be saved
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.required_columns = {
            "employee_id",
            "first_name",
            "last_name",
            "email",
            "hire_date",
            "department_id",
            "department_name",
            "dept_employee_count",
            "dept_earliest_hire",
            "dept_latest_hire",
            "employee_created_at",
            "employee_updated_at",
            "department_created_at",
            "department_updated_at",
        }

    def validate_input_file(self, df: pd.DataFrame) -> bool:
        """
        Validate the input dataframe has all required columns and data types.

        Args:
            df (pd.DataFrame): Input dataframe to validate

        Returns:
            bool: True if validation passes, False otherwise
        """
        # Check for required columns
        missing_columns = self.required_columns - set(df.columns)
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False

        # Check for empty dataframe
        if df.empty:
            logger.error("Input dataframe is empty")
            return False

        # Check for null values in critical columns
        critical_columns = ["employee_id", "first_name", "last_name", "department_id"]
        null_counts = df[critical_columns].isnull().sum()
        if null_counts.any():
            logger.error(
                f"Found null values in critical columns: \n{null_counts[null_counts > 0]}"
            )
            return False

        return True

    def extract_data(self) -> Optional[pd.DataFrame]:
        """
        Extract data from the input CSV file.

        Returns:
            Optional[pd.DataFrame]: Extracted dataframe or None if extraction fails
        """
        try:
            if not self.input_file.exists():
                logger.error(f"Input file not found: {self.input_file}")
                return None

            df = pd.read_csv(self.input_file)
            if not self.validate_input_file(df):
                return None

            logger.info(f"Successfully extracted {len(df)} rows from {self.input_file}")
            return df

        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            return None

    def transform_data(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Transform the input dataframe by applying various data transformations.

        Args:
            df (pd.DataFrame): Input dataframe to transform

        Returns:
            Optional[pd.DataFrame]: Transformed dataframe or None if transformation fails
        """
        try:
            if df is None:
                return None

            transformed_df = df.copy()

            # Convert date columns to datetime
            date_columns = [
                "hire_date",
                "employee_created_at",
                "employee_updated_at",
                "department_created_at",
                "department_updated_at",
                "dept_earliest_hire",
                "dept_latest_hire",
            ]

            for col in date_columns:
                transformed_df[col] = pd.to_datetime(transformed_df[col])

            # Calculate employee tenure
            current_time = datetime.now()
            transformed_df["tenure_days"] = (
                current_time - transformed_df["hire_date"]
            ).dt.days

            # Create full name
            transformed_df["full_name"] = transformed_df.apply(
                lambda x: f"{x['first_name']} {x['last_name']}".strip(), axis=1
            )

            # Calculate department metrics
            transformed_df["department_age_days"] = (
                transformed_df["department_updated_at"]
                - transformed_df["department_created_at"]
            ).dt.days

            # Add tenure category
            tenure_bins = [-float("inf"), 30, 90, 180, float("inf")]
            tenure_labels = ["New Hire", "Early Career", "Established", "Veteran"]

            transformed_df["tenure_category"] = pd.cut(
                transformed_df["tenure_days"], bins=tenure_bins, labels=tenure_labels
            )

            # Calculate time since last update
            transformed_df["days_since_last_update"] = (
                current_time - transformed_df["employee_updated_at"]
            ).dt.days

            # Sort and clean data
            transformed_df = transformed_df.sort_values(
                ["department_name", "hire_date"]
            )
            transformed_df = transformed_df.drop_duplicates(
                subset=["employee_id"], keep="last"
            )

            # Select final columns
            final_columns = [
                "employee_id",
                "full_name",
                "email",
                "hire_date",
                "department_name",
                "dept_employee_count",
                "tenure_days",
                "tenure_category",
                "department_age_days",
                "days_since_last_update",
            ]

            transformed_df = transformed_df[final_columns]

            logger.info(f"Successfully transformed {len(transformed_df)} rows")
            return transformed_df

        except Exception as e:
            logger.error(f"Error during transformation: {str(e)}")
            return None

    def load_data(self, df: pd.DataFrame) -> bool:
        """
        Load the transformed data to the output CSV file.

        Args:
            df (pd.DataFrame): Transformed dataframe to save

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if df is None:
                return False

            # Create output directory if it doesn't exist
            self.output_file.parent.mkdir(parents=True, exist_ok=True)

            # Save to CSV
            df.to_csv(self.output_file, index=False)
            logger.info(f"Successfully saved {len(df)} rows to {self.output_file}")
            return True

        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False

    def run_pipeline(self) -> bool:
        """
        Execute the complete ETL pipeline.

        Returns:
            bool: True if the pipeline completes successfully, False otherwise
        """
        logger.info("Starting ETL pipeline...")

        # Extract
        raw_data = self.extract_data()
        if raw_data is None:
            return False

        # Transform
        transformed_data = self.transform_data(raw_data)
        if transformed_data is None:
            return False

        # Load
        success = self.load_data(transformed_data)

        if success:
            logger.info("ETL pipeline completed successfully!")
        else:
            logger.error("ETL pipeline failed!")

        return success


def main():
    """Main entry point for the ETL pipeline."""
    input_file = "csv/employees-departments_20250423_161401.csv"
    output_file = "output/transformed_employees_data.csv"

    etl = EmployeeETL(input_file, output_file)
    etl.run_pipeline()


if __name__ == "__main__":
    main()
