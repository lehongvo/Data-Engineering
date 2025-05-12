{% macro log_incremental_load() %}
  /*
  Logs information about incremental loads, including:
  - Rows processed
  - Previous max timestamp
  - New max timestamp
  - Duration of load
  - Number of new records
  
  This should be used as a post-hook for incremental models.
  */
  
  {% if model.config.materialized == 'incremental' and is_incremental() %}
    
    {% set get_previous_max_ts %}
      {% if execute %}
        {% set max_col = get_max_loaded_column() %}
        select 
          'Previous load timestamp: ' || coalesce(to_char(max({{ max_col }}), 'YYYY-MM-DD HH24:MI:SS'), 'none') as previous_max_ts,
          count(*) as previous_count
        from {{ this }}
      {% endif %}
    {% endset %}
    
    {% set previous_state = run_query(get_previous_max_ts) %}
    {% set previous_ts = previous_state[0][0] %}
    {% set previous_count = previous_state[0][1] %}
    
    {% set get_current_max_ts %}
      {% if execute %}
        {% set max_col = get_max_loaded_column() %}
        select 
          'Current load timestamp: ' || coalesce(to_char(max({{ max_col }}), 'YYYY-MM-DD HH24:MI:SS'), 'none') as current_max_ts,
          count(*) as current_count
        from {{ this }}
      {% endif %}
    {% endset %}
    
    {% set current_state = run_query(get_current_max_ts) %}
    {% set current_ts = current_state[0][0] %}
    {% set current_count = current_state[0][1] %}
    {% set new_rows = current_count - previous_count %}
    
    {% set incremental_log_query %}
      insert into {{ target.schema }}.incremental_load_log (
        model_name,
        schema_name,
        execution_time_seconds,
        previous_record_count,
        current_record_count,
        new_records_count,
        run_id,
        run_started_at
      )
      values (
        '{{ this.name }}',
        '{{ this.schema }}',
        {{ adapter.get_elapsed_run_time() }},
        {{ previous_count }},
        {{ current_count }},
        {{ new_rows }},
        '{{ run_id }}',
        '{{ run_started_at }}'
      )
    {% endset %}
    
    {% do log_incremental_load_table_if_not_exists() %}
    {% do run_query(incremental_log_query) %}
    
    {% do log_to_file(
        file_path="../../logs/daily/incremental_" ~ this.name ~ "_" ~ modules.datetime.datetime.now().strftime("%Y%m%d") ~ ".log",
        content="Model: " ~ this.name ~ 
                " | Runtime: " ~ adapter.get_elapsed_run_time() ~ " sec" ~
                " | Previous Count: " ~ previous_count ~
                " | Current Count: " ~ current_count ~
                " | New Rows: " ~ new_rows ~
                " | " ~ previous_ts ~
                " | " ~ current_ts ~
                " | Timestamp: " ~ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ) %}
    
  {% endif %}
  
  {{ return('') }}
{% endmacro %}

{% macro log_incremental_load_table_if_not_exists() %}
  /*
  Creates the incremental_load_log table if it doesn't exist
  */
  
  {% set create_table_query %}
    create table if not exists {{ target.schema }}.incremental_load_log (
      id serial primary key,
      model_name varchar(100) not null,
      schema_name varchar(100) not null,
      execution_time_seconds float not null,
      previous_record_count integer not null,
      current_record_count integer not null,
      new_records_count integer not null,
      run_id varchar(100) not null,
      run_started_at timestamp not null,
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(create_table_query) %}
{% endmacro %}

{% macro get_max_loaded_column() %}
  {# 
  Tries to determine the maximum loaded column for an incremental model.
  Looks for common timestamp columns in this order:
  1. updated_at
  2. created_at
  3. order_date
  4. date
  #}
  
  {% set timestamp_columns = ['updated_at', 'created_at', 'order_date', 'date'] %}
  
  {% for col in timestamp_columns %}
    {% set check_col_exists %}
      select count(*)
      from information_schema.columns
      where table_schema = '{{ this.schema }}'
        and table_name = '{{ this.name }}'
        and column_name = '{{ col }}'
    {% endset %}
    
    {% set col_exists = run_query(check_col_exists)[0][0] %}
    
    {% if col_exists > 0 %}
      {% do return(col) %}
    {% endif %}
  {% endfor %}
  
  {# Default to created_at if none of the expected columns exist #}
  {% do return('created_at') %}
{% endmacro %} 