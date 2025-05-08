#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Setup logging for reporting - forced configuration
report_logger = logging.getLogger("reporting")
report_logger.setLevel(logging.INFO)
# Clear any existing handlers to avoid duplicates
if report_logger.handlers:
    report_logger.handlers.clear()
# Set up file handler for reporting
report_handler = logging.FileHandler("logs/report.log", mode='w')
report_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
report_logger.addHandler(report_handler)
# Add console handler for immediate feedback
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
report_logger.addHandler(console_handler)
# Force a test log message
report_logger.info("Reporting logging initialized")

class SparkReporting:
    """Class for creating reports and visualizations from Spark DataFrames."""
    
    def __init__(self, output_dir="output"):
        """Initialize the reporting class with output directory."""
        self.output_dir = output_dir
        self.charts_dir = os.path.join(output_dir, "charts")
        self.reports_dir = os.path.join(output_dir, "reports")
        
        # Create output directories if they don't exist
        os.makedirs(self.charts_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Set plot style
        sns.set_style("whitegrid")
        plt.rcParams.update({'figure.figsize': (10, 6)})
        
        report_logger.info(f"Initialized reporting with output directory: {output_dir}")
        report_logger.info(f"Charts will be saved to: {self.charts_dir}")
        report_logger.info(f"Reports will be saved to: {self.reports_dir}")
    
    def spark_df_to_pandas(self, spark_df):
        """Convert Spark DataFrame to Pandas DataFrame for visualization."""
        report_logger.info("Converting Spark DataFrame to Pandas DataFrame")
        return spark_df.toPandas()
    
    def create_scatter_plot(self, df, x_col, y_col, title, filename=None):
        """
        Create a scatter plot from DataFrame.
        
        Args:
            df: Pandas DataFrame
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Plot title
            filename: Optional filename, if None will be auto-generated
            
        Returns:
            Path to saved plot
        """
        report_logger.info(f"Creating scatter plot: {x_col} vs {y_col}")
        
        # Create plot
        plt.figure(figsize=(10, 6))
        ax = sns.scatterplot(data=df, x=x_col, y=y_col, alpha=0.7)
        
        # Set labels and title
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        
        # Add trendline
        sns.regplot(data=df, x=x_col, y=y_col, scatter=False, ax=ax, color='red')
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scatter_{x_col}_vs_{y_col}_{timestamp}.png"
        
        # Save plot
        filepath = os.path.join(self.charts_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        report_logger.info(f"Scatter plot saved to: {filepath}")
        return filepath
    
    def create_bar_chart(self, df, x_col, y_col, title, filename=None):
        """
        Create a bar chart from DataFrame.
        
        Args:
            df: Pandas DataFrame
            x_col: Column name for x-axis (categories)
            y_col: Column name for y-axis (values)
            title: Plot title
            filename: Optional filename, if None will be auto-generated
            
        Returns:
            Path to saved plot
        """
        report_logger.info(f"Creating bar chart: {y_col} by {x_col}")
        
        # Create plot
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=df, x=x_col, y=y_col)
        
        # Set labels and title
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        
        # Rotate x labels if there are many categories
        if len(df[x_col].unique()) > 5:
            plt.xticks(rotation=45, ha='right')
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bar_{y_col}_by_{x_col}_{timestamp}.png"
        
        # Save plot
        filepath = os.path.join(self.charts_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        report_logger.info(f"Bar chart saved to: {filepath}")
        return filepath
    
    def create_histogram(self, df, col, title, bins=20, filename=None):
        """
        Create a histogram from DataFrame column.
        
        Args:
            df: Pandas DataFrame
            col: Column name to plot
            title: Plot title
            bins: Number of bins
            filename: Optional filename, if None will be auto-generated
            
        Returns:
            Path to saved plot
        """
        report_logger.info(f"Creating histogram for: {col}")
        
        # Create plot
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=col, bins=bins, kde=True)
        
        # Set labels and title
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.title(title)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"histogram_{col}_{timestamp}.png"
        
        # Save plot
        filepath = os.path.join(self.charts_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        report_logger.info(f"Histogram saved to: {filepath}")
        return filepath
    
    def create_html_report(self, title, description, charts=None, tables=None):
        """
        Create an HTML report with charts and tables.
        
        Args:
            title: Report title
            description: Report description
            charts: List of paths to chart images
            tables: List of (table_title, pandas_df) tuples
            
        Returns:
            Path to saved HTML report
        """
        report_logger.info(f"Creating HTML report: {title}")
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.html"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #3498db; margin-top: 30px; }}
                img {{ max-width: 100%; height: auto; margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <p>{description}</p>
        """
        
        # Add charts section if charts are provided
        if charts and len(charts) > 0:
            html_content += "<h2>Charts</h2>"
            for chart_path in charts:
                # Get relative path for the chart
                rel_path = os.path.relpath(chart_path, self.reports_dir)
                chart_name = os.path.basename(chart_path).split('.')[0]
                html_content += f"""
                <div>
                    <h3>{chart_name}</h3>
                    <img src="{rel_path}" alt="{chart_name}">
                </div>
                """
        
        # Add tables section if tables are provided
        if tables and len(tables) > 0:
            html_content += "<h2>Data Tables</h2>"
            for table_title, df in tables:
                html_content += f"<h3>{table_title}</h3>"
                html_content += df.to_html(index=False)
        
        # Close HTML
        html_content += f"""
            <p><small>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        </body>
        </html>
        """
        
        # Write HTML to file
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        report_logger.info(f"HTML report saved to: {filepath}")
        return filepath