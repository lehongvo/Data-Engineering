# Output Directory

This directory contains the processed data output from the Spark job. After running the pipeline, you should see the following subdirectories:

## Expected Subdirectories and Files

1. **Daily Statistics**
   - Directory: `daily_stats/`
   - Content: CSV files with daily statistics per stock
   - Schema:
     ```
     symbol: string
     trade_count: long
     avg_price: double
     min_price: double
     max_price: double
     price_stddev: double
     total_volume: long
     avg_change_percent: double
     ```

2. **Price Movement**
   - Directory: `price_movement/`
   - Content: CSV files with price movement analysis
   - Schema:
     ```
     symbol: string
     first_trade_time: timestamp
     last_trade_time: timestamp
     start_price: double
     end_price: double
     price_change: double
     change_percentage: double
     ```

## Example Data

The output files are in CSV format but are partitioned and have Spark-specific part files like `part-00000-xxxx.csv`. 

A sample record from the daily statistics might look like:
```
"AAPL",27,187.43,163.21,204.76,12.34,143782,0.87
```

A sample record from price movement might look like:
```
"AAPL","2023-08-10 12:34:56","2023-08-10 14:23:45",163.21,167.45,4.24,2.6
```

## Data Warehouse

In addition to these CSV files, the data is also stored in the PostgreSQL data warehouse in tables:
- `stock_daily_stats`
- `stock_price_movement`

You can query these tables using:
```bash
docker-compose exec data-warehouse psql -U datauser -d datawarehouse -c "SELECT * FROM stock_daily_stats LIMIT 5;"
``` 