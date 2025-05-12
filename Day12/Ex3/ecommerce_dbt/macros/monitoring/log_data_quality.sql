{% macro log_data_quality() %}
  /*
  Logs data quality metrics for each model execution, including:
  - Null count for key columns
  - Unique count for key columns
  - Min/max values for important metrics
  - Duplicate check results
  
  This should be used as a post-hook for models where data quality monitoring is important.
  */
  
  {% set model_name = this.name %}
  {% set schema_name = this.schema %}
  
  {# Determine model type and set appropriate columns to check #}
  {% if 'dim_' in model_name %}
    {% set model_type = 'dimension' %}
    {% if model_name == 'dim_customers' or model_name == 'dim_customers_mart' %}
      {% set key_column = 'customer_id' %}
      {% set metric_columns = ['lifetime_value', 'lifetime_orders'] %}
    {% elif model_name == 'dim_products' or model_name == 'dim_products_mart' %}
      {% set key_column = 'product_id' %}
      {% set metric_columns = ['price', 'total_quantity_sold', 'total_revenue'] %}
    {% elif model_name == 'dim_date' %}
      {% set key_column = 'date_key' %}
      {% set metric_columns = [] %}
    {% else %}
      {% set key_column = 'id' %}
      {% set metric_columns = [] %}
    {% endif %}
  {% elif 'fct_' in model_name %}
    {% set model_type = 'fact' %}
    {% if model_name == 'fct_orders' %}
      {% set key_column = 'order_id' %}
      {% set metric_columns = ['total_amount', 'total_items'] %}
    {% elif model_name == 'fct_order_items' %}
      {% set key_column = 'order_item_id' %}
      {% set metric_columns = ['quantity', 'unit_price', 'item_total'] %}
    {% elif model_name == 'fct_daily_sales' %}
      {% set key_column = 'date_key' %}
      {% set metric_columns = ['total_sales_amount', 'orders_count', 'customers_count'] %}
    {% elif model_name == 'fct_monthly_sales' %}
      {% set key_column = 'year_month' %}
      {% set metric_columns = ['total_sales_amount', 'orders_count', 'unique_customers'] %}
    {% elif model_name == 'fct_customer_retention' %}
      {% set key_column = 'cohort' %}
      {% set metric_columns = ['cohort_size', 'retained_customers', 'retention_rate'] %}
    {% else %}
      {% set key_column = 'id' %}
      {% set metric_columns = [] %}
    {% endif %}
  {% else %}
    {% set model_type = 'other' %}
    {% set key_column = 'id' %}
    {% set metric_columns = [] %}
  {% endif %}
  
  {# Check if key column exists #}
  {% set check_key_exists %}
    select count(*)
    from information_schema.columns
    where table_schema = '{{ this.schema }}'
      and table_name = '{{ this.name }}'
      and column_name = '{{ key_column }}'
  {% endset %}
  
  {% set key_exists = run_query(check_key_exists)[0][0] %}
  
  {% if key_exists > 0 %}
    {# Get null count for key column #}
    {% set null_count_query %}
      select count(*) 
      from {{ this }}
      where {{ key_column }} is null
    {% endset %}
    
    {% set null_count = run_query(null_count_query)[0][0] %}
    
    {# Check for duplicates in key column #}
    {% set dup_check_query %}
      select count(*) - count(distinct {{ key_column }})
      from {{ this }}
      where {{ key_column }} is not null
    {% endset %}
    
    {% set dup_count = run_query(dup_check_query)[0][0] %}
    
    {# Get total row count #}
    {% set row_count_query %}
      select count(*) from {{ this }}
    {% endset %}
    
    {% set row_count = run_query(row_count_query)[0][0] %}
    
    {# Log basic data quality metrics #}
    {% set data_quality_log_query %}
      insert into {{ target.schema }}.data_quality_log (
        model_name,
        schema_name,
        model_type,
        key_column,
        row_count,
        null_count,
        duplicate_count,
        run_id,
        run_started_at
      )
      values (
        '{{ this.name }}',
        '{{ this.schema }}',
        '{{ model_type }}',
        '{{ key_column }}',
        {{ row_count }},
        {{ null_count }},
        {{ dup_count }},
        '{{ run_id }}',
        '{{ run_started_at }}'
      )
    {% endset %}
    
    {% do log_data_quality_table_if_not_exists() %}
    {% do run_query(data_quality_log_query) %}
    
    {# Log detailed metrics for each metric column #}
    {% for metric_col in metric_columns %}
      {% set check_col_exists %}
        select count(*)
        from information_schema.columns
        where table_schema = '{{ this.schema }}'
          and table_name = '{{ this.name }}'
          and column_name = '{{ metric_col }}'
      {% endset %}
      
      {% set col_exists = run_query(check_col_exists)[0][0] %}
      
      {% if col_exists > 0 %}
        {% set metric_stats_query %}
          select
            '{{ metric_col }}' as metric_name,
            sum(case when {{ metric_col }} is null then 1 else 0 end) as null_count,
            min({{ metric_col }}) as min_value,
            max({{ metric_col }}) as max_value,
            avg({{ metric_col }}) as avg_value,
            count(distinct {{ metric_col }}) as distinct_count
          from {{ this }}
        {% endset %}
        
        {% set metric_stats = run_query(metric_stats_query) %}
        
        {% set metric_log_query %}
          insert into {{ target.schema }}.data_quality_metrics_log (
            model_name,
            schema_name,
            metric_name,
            null_count,
            min_value,
            max_value,
            avg_value,
            distinct_count,
            run_id
          )
          values (
            '{{ this.name }}',
            '{{ this.schema }}',
            '{{ metric_stats[0][0] }}',
            {{ metric_stats[0][1] }},
            {{ metric_stats[0][2] }},
            {{ metric_stats[0][3] }},
            {{ metric_stats[0][4] }},
            {{ metric_stats[0][5] }},
            '{{ run_id }}'
          )
        {% endset %}
        
        {% do log_data_quality_metrics_table_if_not_exists() %}
        {% do run_query(metric_log_query) %}
      {% endif %}
    {% endfor %}
    
    {# Log to file #}
    {% set file_content = "Model: " ~ this.name ~ 
      " | Type: " ~ model_type ~
      " | Rows: " ~ row_count ~
      " | Key: " ~ key_column ~
      " | Nulls: " ~ null_count ~
      " | Duplicates: " ~ dup_count ~
      " | Time: " ~ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") %}
    
    {% do log_to_file(
        file_path="../../logs/daily/data_quality_" ~ this.name ~ "_" ~ modules.datetime.datetime.now().strftime("%Y%m%d") ~ ".log",
        content=file_content
    ) %}
    
    {# Alert on data quality issues #}
    {% if null_count > 0 or dup_count > 0 %}
      {% do log_to_file(
          file_path="../../logs/audit/data_quality_alerts_" ~ modules.datetime.datetime.now().strftime("%Y%m%d") ~ ".log",
          content="[ALERT] " ~ file_content
      ) %}
    {% endif %}
  {% endif %}
  
  {{ return('') }}
{% endmacro %}

{% macro log_data_quality_table_if_not_exists() %}
  /*
  Creates the data_quality_log table if it doesn't exist
  */
  
  {% set create_table_query %}
    create table if not exists {{ target.schema }}.data_quality_log (
      id serial primary key,
      model_name varchar(100) not null,
      schema_name varchar(100) not null,
      model_type varchar(50) not null,
      key_column varchar(100) not null,
      row_count integer not null,
      null_count integer not null,
      duplicate_count integer not null,
      run_id varchar(100) not null,
      run_started_at timestamp not null,
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(create_table_query) %}
{% endmacro %}

{% macro log_data_quality_metrics_table_if_not_exists() %}
  /*
  Creates the data_quality_metrics_log table if it doesn't exist
  */
  
  {% set create_table_query %}
    create table if not exists {{ target.schema }}.data_quality_metrics_log (
      id serial primary key,
      model_name varchar(100) not null,
      schema_name varchar(100) not null,
      metric_name varchar(100) not null,
      null_count integer not null,
      min_value numeric,
      max_value numeric,
      avg_value numeric,
      distinct_count integer,
      run_id varchar(100) not null,
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(create_table_query) %}
{% endmacro %} 