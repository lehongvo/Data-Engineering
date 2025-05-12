{% macro log_test_results(test_name, test_status, test_rows, message='') %}
  /*
  Logs test execution details to a database table and a file
  
  Arguments:
    test_name: Name of the test
    test_status: Test result status ('pass' or 'fail')
    test_rows: Number of rows that failed the test
    message: Optional message with additional details
  */
  
  {% set test_execution_log_query %}
    insert into {{ target.schema }}.test_execution_log (
      test_name,
      test_type,
      test_status,
      failure_count,
      error_message,
      run_id,
      run_started_at,
      node_id,
      model_name
    )
    values (
      '{{ test_name }}',
      '{{ test.test_metadata.name if "test_metadata" in test else "unknown" }}',
      '{{ test_status }}',
      {{ test_rows }},
      '{{ message | replace("'", "''") }}',
      '{{ run_id }}',
      '{{ run_started_at }}',
      '{{ node.unique_id }}',
      '{{ node.refs[0][0] if node.refs and node.refs[0] else "unknown" }}'
    )
  {% endset %}
  
  {% do log_test_execution_table_if_not_exists() %}
  {% do run_query(test_execution_log_query) %}
  
  {% do log_to_file(
      file_path="../../logs/daily/test_results_" ~ modules.datetime.datetime.now().strftime("%Y%m%d") ~ ".log",
      content="Test: " ~ test_name ~ 
              " | Status: " ~ test_status ~ 
              " | Failed Rows: " ~ test_rows ~ 
              " | Timestamp: " ~ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ~
              ((" | Message: " ~ message) if message else "")
  ) %}
  
  -- If the test failed, log more detailed information to a separate failure log
  {% if test_status == 'fail' %}
    {% do log_to_file(
        file_path="../../logs/audit/test_failures_" ~ modules.datetime.datetime.now().strftime("%Y%m%d") ~ ".log",
        content="[FAILURE] Test: " ~ test_name ~ 
                " | Failed Rows: " ~ test_rows ~ 
                " | Model: " ~ node.refs[0][0] if node.refs and node.refs[0] else "unknown" ~
                " | Timestamp: " ~ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ~
                " | Details: " ~ message
    ) %}
  {% endif %}
  
  {{ return('') }}
{% endmacro %}

{% macro log_test_execution_table_if_not_exists() %}
  /*
  Creates the test_execution_log table if it doesn't exist
  */
  
  {% set create_table_query %}
    create table if not exists {{ target.schema }}.test_execution_log (
      id serial primary key,
      test_name varchar(100) not null,
      test_type varchar(100),
      test_status varchar(20) not null,
      failure_count integer not null,
      error_message text,
      run_id varchar(100) not null,
      run_started_at timestamp not null,
      node_id varchar(100) not null,
      model_name varchar(100),
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(create_table_query) %}
{% endmacro %} 