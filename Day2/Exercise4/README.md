# Employee Data ETL Pipeline

This ETL (Extract-Transform-Load) pipeline processes employee and department data from a CSV file, performs various transformations, and loads the results into a new CSV file.

## Features

- Extract data from employee-department CSV files
- Transform data by:
  - Converting date fields to proper datetime format
  - Calculating employee tenure and categorizing it
  - Creating full name from first and last names
  - Calculating department age and metrics
  - Adding time-based analytics
  - Cleaning and organizing data
- Load transformed data to a new CSV file

## Requirements

- Python 3.7+
- pandas
- numpy

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Ensure your input CSV file is in the correct location (default: csv/employees-departments_20250423_161401.csv)
2. Run the ETL pipeline:
```bash
python etl_pipeline.py
```

The script will:
1. Read data from the input CSV file
2. Transform the data
3. Save the results to `transformed_employees_data.csv`

## Input Data Format

The input CSV file should have the following columns:
- employee_id
- first_name
- last_name
- email
- hire_date
- department_id
- department_name
- dept_employee_count
- dept_earliest_hire
- dept_latest_hire
- employee_created_at
- employee_updated_at
- department_created_at
- department_updated_at

## Output Data Format

The transformed data will be saved with the following columns:
- employee_id
- full_name (combined first and last name)
- email
- hire_date
- department_name
- dept_employee_count
- tenure_days (calculated from hire_date)
- tenure_category (New Hire/Early Career/Established/Veteran)
- department_age_days
- days_since_last_update

## Transformations Applied

1. Date Conversions: All date fields are converted to proper datetime format
2. Tenure Calculation: Employee tenure is calculated in days
3. Tenure Categories:
   - New Hire: < 30 days
   - Early Career: 30-90 days
   - Established: 90-180 days
   - Veteran: > 180 days
4. Department Analytics: Department age calculation
5. Data Cleaning: Removal of duplicate employee records
6. Data Organization: Sorting by department and hire date 