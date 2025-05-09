#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flink Word Count Example - Tối ưu
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.udf import udf
from pyflink.common.typeinfo import Types

import re
import os

def create_input_table(t_env, input_path):
    # Define the input DDL
    input_ddl = f"""
        CREATE TABLE input_table (
            line STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{input_path}',
            'format' = 'text'
        )
    """
    t_env.execute_sql(input_ddl)
    return t_env.from_path("input_table")

def create_output_table(t_env, output_path):
    # Define the output DDL
    output_ddl = f"""
        CREATE TABLE output_table (
            word STRING,
            count BIGINT
        ) WITH (
            'connector' = 'filesystem',
            'path' = '{output_path}',
            'format' = 'csv'
        )
    """
    t_env.execute_sql(output_ddl)
    return

def main():
    # Create execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # Set parallelism to 1 for easy debugging
    env.set_parallelism(1)
    
    # Create a Table environment - sử dụng batch mode cho WordCount
    settings = EnvironmentSettings.new_instance() \
        .in_batch_mode() \
        .build()
    
    # Create a TableEnvironment
    t_env = StreamTableEnvironment.create(env, settings)
    
    # Register UDF to tokenize text
    @udf(result_type=Types.ARRAY(Types.STRING()))
    def tokenize(line):
        # Đơn giản hóa xử lý từ
        return re.sub(r'[^\w\s]', ' ', line.lower()).split()
    
    # Register UDF
    t_env.create_temporary_function("tokenize", tokenize)
    
    # Set input and output paths
    input_path = "/data/input.txt"
    output_path = "/data/output"
    
    # Clean output directory if it exists
    try:
        os.makedirs(f"/data/output", exist_ok=True)
    except Exception as e:
        print(f"Warning when creating output directory: {e}")
    
    # Create tables
    input_table = create_input_table(t_env, input_path)
    create_output_table(t_env, output_path)
    
    # Process data: tokenize, count words and insert into output table
    word_count_sql = """
        INSERT INTO output_table
        SELECT word, COUNT(*) as count
        FROM (
            SELECT word
            FROM input_table,
            LATERAL TABLE(tokenize(line)) AS T(word)
            WHERE word <> ''
        )
        GROUP BY word
    """
    
    print("Starting Word Count job...")
    
    # Execute the SQL
    t_env.execute_sql(word_count_sql).wait()
    
    print("Job executed successfully! Results are stored in /data/output directory.")

if __name__ == "__main__":
    main() 