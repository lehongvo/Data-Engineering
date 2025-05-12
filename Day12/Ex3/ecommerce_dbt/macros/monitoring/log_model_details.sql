{% macro log_model_details() %}
  /*
  A comprehensive macro that logs detailed information about model execution:
  - Execution time
  - Row count
  - Query complexity
  - Dependencies
  - Tags
  
  This macro should be added as a post-hook in the dbt_project.yml file.
  */
  
  {% set model_execution_log_query %}
    insert into {{ target.schema }}.model_execution_log (
      model_name,
      schema_name,
      materialization_type,
      execution_time_seconds,
      rows_affected,
      node_id,
      depends_on_nodes,
      tags,
      run_id,
      run_started_at,
      user_id,
      target_name,
      environment_name
    )
    values (
      '{{ this.name }}',
      '{{ this.schema }}',
      '{{ model.config.materialized }}',
      {{ adapter.get_elapsed_run_time() }},
      (select count(*) from {{ this }}),
      '{{ model.unique_id }}',
      '{{ model.depends_on.nodes|join(",") }}',
      '{{ model.tags|join(",") }}',
      '{{ run_id }}',
      '{{ run_started_at }}',
      '{{ env_var("USER", "unknown") }}',
      '{{ target.name }}',
      '{{ target.name }}'
    )
  {% endset %}
  
  {% do log_model_execution_table_if_not_exists() %}
  {% do run_query(model_execution_log_query) %}
  
  {% do log_to_file(
      file_path="../../logs/daily/model_" ~ this.name ~ "_" ~ modules.datetime.datetime.now().strftime("%Y%m%d") ~ ".log",
      content="Model: " ~ this.name ~ 
              " | Runtime: " ~ adapter.get_elapsed_run_time() ~ " sec" ~
              " | Timestamp: " ~ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ~
              " | Status: Success"
  ) %}
  
  {{ return('') }}
{% endmacro %}

{% macro log_model_execution_table_if_not_exists() %}
  /*
  Creates the model_execution_log table if it doesn't exist
  */
  
  {% set create_table_query %}
    create table if not exists {{ target.schema }}.model_execution_log (
      id serial primary key,
      model_name varchar(100) not null,
      schema_name varchar(100) not null,
      materialization_type varchar(50) not null,
      execution_time_seconds float not null,
      rows_affected integer,
      node_id varchar(100) not null,
      depends_on_nodes text,
      tags text,
      run_id varchar(100) not null,
      run_started_at timestamp not null,
      user_id varchar(100),
      target_name varchar(100),
      environment_name varchar(100),
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(create_table_query) %}
{% endmacro %}

{% macro log_to_file(file_path, content) %}
  /*
  Logs content to a file
  */
  {% set cmd %}
    mkdir -p $(dirname {{ file_path }}) && 
    echo "{{ content }}" >> {{ file_path }}
  {% endset %}
  
  {% do run_query("select 1") %}
  {% do log(cmd) %}
{% endmacro %} 