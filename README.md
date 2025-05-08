# BigQuery-Spark Integration for Data Analysis

This project demonstrates how to integrate Google BigQuery with Apache Spark to perform large-scale data analysis.

## Overview

The project covers four main aspects:

1. **Extracting Data from BigQuery**: Pull data from BigQuery into Spark environment for processing
2. **Complex Analysis with Spark**: Apply complex data operations on large datasets using Spark
3. **Optimized Writing to BigQuery**: Write results back to BigQuery in high-performance format
4. **Reporting from Results**: Create visual analytics reports from the processed data

## Prerequisites

- Google Cloud account with BigQuery access
- Apache Spark installed
- Python 3.8+ with PySpark
- Google Cloud SDK

## Setup

1. Place your Google Cloud service account key in `config/account_key.json`
2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Make the run script executable:
   ```
   chmod +x run.sh
   ```

## Running the Project

```bash
./run.sh
```

## Directory Structure

```
Exercise5/
├── config/             # Configuration files
│   └── account_key.json  # Google Cloud service account key
├── src/                # Source code
│   ├── bigquery_spark_integration.py  # Main integration script
│   ├── data_analysis.py               # Data analysis functions
│   └── reporting.py                   # Reporting utilities
├── data/               # Sample data and downloaded files
├── logs/               # Application logs
├── output/             # Analysis results
└── screenshots/        # Screenshots of results
```

## Learning Resources

- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Google Cloud BigQuery Connector for Spark](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)