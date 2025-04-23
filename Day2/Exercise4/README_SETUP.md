# ETL Pipeline Setup and Usage Guide

## Prerequisites

Make sure you have Python 3.7+ installed on your system. You can check your Python version with:
```bash
python3 --version
```

## Project Setup

### 1. Clone the Repository (if applicable)
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Set Up Virtual Environment

Create a new virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:

For macOS/Linux:
```bash
source venv/bin/activate
```

For Windows:
```bash
.\venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt after activation.

### 3. Install Dependencies

Install required packages:
```bash
pip install pandas numpy
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Running the ETL Pipeline

### 1. Prepare Input Data
Ensure your input CSV file is in the correct location:
```bash
csv/employees-departments_20250423_161401.csv
```

### 2. Run the Pipeline
```bash
python3 etl_pipeline.py
```

The script will:
- Read data from the input CSV
- Perform transformations
- Save results to `output/transformed_employees_data.csv`
- Create logs in `etl_pipeline.log`

## Directory Structure
```
.
├── csv/
│   └── employees-departments_20250423_161401.csv
├── output/
│   └── transformed_employees_data.csv
├── venv/
├── etl_pipeline.py
├── requirements.txt
└── etl_pipeline.log
```

## Common Commands

### Package Management

Update pip:
```bash
pip install --upgrade pip
```

List installed packages:
```bash
pip list
```

Export dependencies:
```bash
pip freeze > requirements.txt
```

### Virtual Environment

Deactivate virtual environment:
```bash
deactivate
```

Remove virtual environment:
```bash
rm -rf venv
```

Create new virtual environment with specific Python version:
```bash
python3.9 -m venv venv
```

### File Operations

Check log file:
```bash
tail -f etl_pipeline.log
```

Check output file:
```bash
head -n 5 output/transformed_employees_data.csv
```

## Troubleshooting

### 1. Python Command Not Found
If `python3` command is not found:
```bash
# For macOS (using Homebrew)
brew install python3
```

### 2. Permission Issues
If you encounter permission issues:
```bash
chmod +x etl_pipeline.py
```

### 3. Module Not Found Errors
If you get "Module not found" errors, verify you're in the virtual environment:
```bash
# Should show path to venv
which python
```

Then reinstall dependencies:
```bash
pip install -r requirements.txt
```

### 4. Data Directory Issues
Create required directories if missing:
```bash
mkdir -p csv output
```

## Maintenance

### Clean Up

Remove generated files:
```bash
rm -f output/*.csv
rm -f etl_pipeline.log
```

Remove all Python cache files:
```bash
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
```

### Update Dependencies

Update all packages:
```bash
pip install --upgrade -r requirements.txt
```

## Development Commands

### Code Formatting
If using black for code formatting:
```bash
pip install black
black etl_pipeline.py
```

### Linting
If using flake8 for linting:
```bash
pip install flake8
flake8 etl_pipeline.py
```

### Type Checking
If using mypy for type checking:
```bash
pip install mypy
mypy etl_pipeline.py
```

## Production Deployment

### Create Production Requirements
```bash
pip install pip-tools
pip-compile requirements.in
```

### Run with Production Settings
```bash
python3 etl_pipeline.py --env production
```

## Monitoring

### Check Process Status
```bash
ps aux | grep etl_pipeline.py
```

### Monitor Log File
```bash
tail -f etl_pipeline.log | grep ERROR
```

### Check Disk Usage
```bash
du -h output/
``` 