{% macro setup_monitoring() %}
  /*
  A master macro that initializes all monitoring tables and directories.
  This should be run at the start of a dbt job.
  */
  
  {% set monitoring_tables = [
    {
      "name": "dbt_run_log",
      "columns": [
        "id serial primary key",
        "run_id varchar(100) not null",
        "invocation_id varchar(100) not null",
        "start_time timestamp not null",
        "end_time timestamp",
        "status varchar(20)",
        "duration_seconds float",
        "models_executed integer",
        "tests_executed integer",
        "user_id varchar(100)",
        "target_name varchar(100)",
        "environment_name varchar(100)",
        "dbt_version varchar(50)",
        "command varchar(100)",
        "run_args text",
        "created_at timestamp default current_timestamp"
      ]
    }
  ] %}
  
  {% for table in monitoring_tables %}
    {% set create_table_query %}
      create table if not exists {{ target.schema }}.{{ table.name }} (
        {{ table.columns | join(", ") }}
      )
    {% endset %}
    
    {% do run_query(create_table_query) %}
  {% endfor %}
  
  {# Log run start #}
  {% set insert_run_start %}
    insert into {{ target.schema }}.dbt_run_log (
      run_id,
      invocation_id,
      start_time,
      user_id,
      target_name,
      environment_name,
      dbt_version,
      command,
      run_args
    ) values (
      '{{ run_id }}',
      '{{ invocation_id }}',
      '{{ run_started_at }}',
      '{{ env_var("USER", "unknown") }}',
      '{{ target.name }}',
      '{{ target.name }}',
      '{{ dbt_version }}',
      '{{ flags.WHICH }}',
      '{{ flags.ARGS }}'
    )
  {% endset %}
  
  {% do run_query(insert_run_start) %}
  
  {# Initialize log files #}
  {% set log_dirs = [
    "../../logs/daily",
    "../../logs/audit",
    "../../reports/performance",
    "../../reports/metrics",
    "../../reports/jobs"
  ] %}
  
  {% for dir in log_dirs %}
    {% set mkdir_cmd %}mkdir -p {{ dir }}{% endset %}
    {% do log(mkdir_cmd) %}
  {% endfor %}
  
  {% do log_to_file(
    file_path="../../logs/daily/run_start_" ~ modules.datetime.datetime.now().strftime("%Y%m%d_%H%M%S") ~ ".log",
    content="Run started: " ~ run_started_at ~ 
            " | Run ID: " ~ run_id ~ 
            " | Command: " ~ flags.WHICH ~ 
            " | User: " ~ env_var("USER", "unknown")
  ) %}
  
  {{ return('') }}
{% endmacro %}

{% macro finish_monitoring() %}
  /*
  Finalize monitoring by:
  - Updating the run log with completion information
  - Running database performance monitoring
  - Generating summary reports
  */
  
  {# Update run log with completion information #}
  {% set update_run_log %}
    update {{ target.schema }}.dbt_run_log
    set
      end_time = current_timestamp,
      status = 'completed',
      duration_seconds = extract(epoch from (current_timestamp - start_time)),
      models_executed = (select count(*) from {{ target.schema }}.model_execution_log where run_id = '{{ run_id }}'),
      tests_executed = (select count(*) from {{ target.schema }}.test_execution_log where run_id = '{{ run_id }}')
    where run_id = '{{ run_id }}'
      and end_time is null
  {% endset %}
  
  {% do run_query(update_run_log) %}
  
  {# Run database performance monitoring #}
  {% do monitor_db_performance() %}
  
  {# Generate summary report #}
  {% set get_model_execution_stats %}
    select
      count(*) as total_models,
      sum(execution_time_seconds) as total_execution_time,
      avg(execution_time_seconds) as avg_execution_time,
      max(execution_time_seconds) as max_execution_time,
      sum(rows_affected) as total_rows
    from {{ target.schema }}.model_execution_log
    where run_id = '{{ run_id }}'
  {% endset %}
  
  {% set model_stats = run_query(get_model_execution_stats) %}
  
  {% set get_test_execution_stats %}
    select
      count(*) as total_tests,
      count(case when test_status = 'pass' then 1 end) as passed_tests,
      count(case when test_status = 'fail' then 1 end) as failed_tests,
      sum(failure_count) as total_failures
    from {{ target.schema }}.test_execution_log
    where run_id = '{{ run_id }}'
  {% endset %}
  
  {% set test_stats = run_query(get_test_execution_stats) %}
  
  {% set get_run_info %}
    select
      duration_seconds,
      models_executed,
      tests_executed
    from {{ target.schema }}.dbt_run_log
    where run_id = '{{ run_id }}'
  {% endset %}
  
  {% set run_info = run_query(get_run_info) %}
  
  {% set get_slow_models %}
    select
      model_name,
      execution_time_seconds,
      rows_affected
    from {{ target.schema }}.model_execution_log
    where run_id = '{{ run_id }}'
    order by execution_time_seconds desc
    limit 5
  {% endset %}
  
  {% set slow_models = run_query(get_slow_models) %}
  
  {% set report_content %}
Run Summary Report
=================
Date: {{ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") }}
Run ID: {{ run_id }}
Duration: {{ run_info[0][0]|round(2) }} seconds

Execution Statistics
-------------------
Models Executed: {{ run_info[0][1] }}
Tests Executed: {{ run_info[0][2] }}
Total Rows Processed: {{ model_stats[0][4] }}

Model Performance
----------------
Total Model Execution Time: {{ model_stats[0][1]|round(2) }} seconds
Average Model Execution Time: {{ model_stats[0][2]|round(2) }} seconds
Maximum Model Execution Time: {{ model_stats[0][3]|round(2) }} seconds

Test Results
-----------
Tests Passed: {{ test_stats[0][1] }}
Tests Failed: {{ test_stats[0][2] }}
Total Test Failures: {{ test_stats[0][3] }}

Slowest Models
-------------
{% for model in slow_models %}
{{ loop.index }}. {{ model[0] }} - {{ model[1]|round(2) }} seconds ({{ model[2] }} rows)
{% endfor %}
  {% endset %}
  
  {% do log_to_file(
    file_path="../../reports/jobs/run_summary_" ~ modules.datetime.datetime.now().strftime("%Y%m%d_%H%M%S") ~ ".md",
    content=report_content
  ) %}
  
  {% do log_to_file(
    file_path="../../logs/daily/run_completed_" ~ modules.datetime.datetime.now().strftime("%Y%m%d_%H%M%S") ~ ".log",
    content="Run completed: " ~ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ~ 
            " | Run ID: " ~ run_id ~ 
            " | Duration: " ~ run_info[0][0]|round(2) ~ " seconds" ~
            " | Models: " ~ run_info[0][1] ~ 
            " | Tests: " ~ run_info[0][2] ~ 
            " | Tests Failed: " ~ test_stats[0][2]
  ) %}
  
  {{ return('') }}
{% endmacro %}

{% macro on_run_start() %}
  /*
  To be used as a macro that runs at the start of a dbt run (on-run-start hook)
  */
  {{ setup_monitoring() }}
  {{ return('') }}
{% endmacro %}

{% macro on_run_end() %}
  /*
  To be used as a macro that runs at the end of a dbt run (on-run-end hook)
  */
  {{ finish_monitoring() }}
  {{ return('') }}
{% endmacro %} 