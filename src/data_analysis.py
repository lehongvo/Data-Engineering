#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, avg, sum, count, stddev, rank, desc, window, expr
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Setup logging for data analysis - forced configuration
analysis_logger = logging.getLogger("data-analysis")
analysis_logger.setLevel(logging.INFO)
# Clear any existing handlers to avoid duplicates
if analysis_logger.handlers:
    analysis_logger.handlers.clear()
# Add file handler
analysis_handler = logging.FileHandler("logs/analysis.log")
analysis_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
analysis_logger.addHandler(analysis_handler)
# Add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
analysis_logger.addHandler(console_handler)
# Force a test log message
analysis_logger.info("Data Analysis logging initialized")

def perform_time_series_analysis(df, timestamp_col, value_col, window_duration="1 day"):
    """
    Perform time series analysis on data using Spark window functions.
    
    Args:
        df: Input Spark DataFrame
        timestamp_col: Column name containing timestamp
        value_col: Column name containing the value to analyze
        window_duration: Window duration for aggregation (e.g., "1 day", "1 hour")
        
    Returns:
        DataFrame with time series analysis results
    """
    analysis_logger.info(f"Performing time series analysis on {value_col} with window {window_duration}")
    
    # Ensure timestamp is in timestamp format
    if df.schema[timestamp_col].dataType.typeName() != "timestamp":
        df = df.withColumn(timestamp_col, expr(f"CAST({timestamp_col} AS TIMESTAMP)"))
    
    # Perform window aggregations
    result = df.withWatermark(timestamp_col, window_duration) \
        .groupBy(window(col(timestamp_col), window_duration)) \
        .agg(
            avg(col(value_col)).alias(f"avg_{value_col}"),
            sum(col(value_col)).alias(f"sum_{value_col}"),
            count(col(value_col)).alias("count"),
            stddev(col(value_col)).alias(f"stddev_{value_col}")
        ) \
        .orderBy("window")
    
    return result

def identify_anomalies(df, value_col, threshold=3.0):
    """
    Identify anomalies in data using Z-score method.
    
    Args:
        df: Input Spark DataFrame
        value_col: Column name containing the value to analyze
        threshold: Z-score threshold for anomaly detection
        
    Returns:
        DataFrame with anomalies flagged
    """
    analysis_logger.info(f"Identifying anomalies in {value_col} with threshold {threshold}")
    
    # Calculate mean and standard deviation
    stats = df.select(
        avg(col(value_col)).alias("mean"),
        stddev(col(value_col)).alias("stddev")
    ).collect()[0]
    
    mean = stats["mean"]
    stddev = stats["stddev"]
    
    # Flag anomalies using Z-score
    result = df.withColumn(
        "z_score", 
        (col(value_col) - mean) / stddev
    ).withColumn(
        "is_anomaly",
        (col("z_score").abs() > threshold)
    )
    
    return result

def perform_clustering(df, feature_cols, k=3):
    """
    Perform K-means clustering on data.
    
    Args:
        df: Input Spark DataFrame
        feature_cols: List of column names to use as features
        k: Number of clusters
        
    Returns:
        DataFrame with cluster assignments and cluster centers
    """
    analysis_logger.info(f"Performing clustering with {len(feature_cols)} features and k={k}")
    
    # Assemble features into a vector
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    assembled_df = assembler.transform(df)
    
    # Train KMeans model
    kmeans = KMeans(k=k, seed=42)
    model = kmeans.fit(assembled_df)
    
    # Add cluster predictions to the DataFrame
    predictions = model.transform(assembled_df)
    
    # Evaluate clustering
    evaluator = ClusteringEvaluator()
    silhouette = evaluator.evaluate(predictions)
    analysis_logger.info(f"Clustering silhouette with squared euclidean distance: {silhouette}")
    
    return predictions, model.clusterCenters()

def find_top_correlations(df, target_col, num_cols=10):
    """
    Find columns with highest correlation to a target column.
    
    Args:
        df: Input Spark DataFrame
        target_col: Target column name to correlate against
        num_cols: Number of top correlations to return
        
    Returns:
        List of (column_name, correlation) tuples
    """
    analysis_logger.info(f"Finding top correlations with {target_col}")
    
    # Get numerical columns
    numeric_cols = [f.name for f in df.schema.fields 
                   if f.dataType.typeName() in ["double", "integer", "long", "float"]
                   and f.name != target_col]
    
    correlations = []
    for col_name in numeric_cols:
        correlation = df.stat.corr(target_col, col_name)
        correlations.append((col_name, correlation))
    
    # Sort by absolute correlation value
    sorted_correlations = sorted(correlations, key=lambda x: abs(x[1]), reverse=True)
    
    return sorted_correlations[:num_cols]

def segment_and_analyze(df, segment_col, value_col):
    """
    Segment data and perform comparative analysis.
    
    Args:
        df: Input Spark DataFrame
        segment_col: Column to segment by
        value_col: Value column to analyze
        
    Returns:
        DataFrame with segment analysis
    """
    analysis_logger.info(f"Segmenting data by {segment_col} and analyzing {value_col}")
    
    # Group by segment and calculate statistics
    segment_analysis = df.groupBy(segment_col) \
        .agg(
            count("*").alias("count"),
            avg(col(value_col)).alias(f"avg_{value_col}"),
            sum(col(value_col)).alias(f"sum_{value_col}"),
            stddev(col(value_col)).alias(f"stddev_{value_col}")
        ) \
        .orderBy(desc("count"))
    
    return segment_analysis

def rank_within_groups(df, group_col, rank_col, rank_name="rank", ascending=False):
    """
    Rank values within groups.
    
    Args:
        df: Input Spark DataFrame
        group_col: Column to group by
        rank_col: Column to rank
        rank_name: Name for the new rank column
        ascending: If True, smallest values get lowest ranks
        
    Returns:
        DataFrame with added rank column
    """
    analysis_logger.info(f"Ranking {rank_col} within groups of {group_col}")
    
    # Define window specification
    window_spec = Window.partitionBy(group_col).orderBy(col(rank_col).desc() if not ascending else col(rank_col))
    
    # Add rank column
    result = df.withColumn(rank_name, rank().over(window_spec))
    
    return result