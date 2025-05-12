{% macro log_model_timing() %}
  /*
  A macro that logs the execution time of each model.
  This macro should be added as a post-hook in the dbt_project.yml file.
  
  Example usage in dbt_project.yml:
    models:
      +post-hook: "{{ log_model_timing() }}"
  */
  
  {% set query %}
    insert into {{ target.schema }}.model_timing_log (
      model_name,
      schema_name,
      execution_time_seconds,
      node_id,
      run_id,
      run_started_at
    )
    values (
      '{{ this.name }}',
      '{{ this.schema }}',
      {{ adapter.get_elapsed_run_time() }},
      '{{ model.unique_id }}',
      '{{ run_id }}',
      '{{ run_started_at }}'
    )
  {% endset %}
  
  {% if target.name != 'dev' %}
    -- Only log timing in production environments
    {% do run_query(create_log_table_if_not_exists()) %}
    {% do run_query(query) %}
  {% endif %}
  
  {{ return('') }}
{% endmacro %}

{% macro create_log_table_if_not_exists() %}
  /*
  Creates the model_timing_log table if it doesn't exist
  */
  
  {% set create_table_query %}
    create table if not exists {{ target.schema }}.model_timing_log (
      id serial primary key,
      model_name varchar(100) not null,
      schema_name varchar(100) not null,
      execution_time_seconds float not null,
      node_id varchar(100) not null,
      run_id varchar(100) not null,
      run_started_at timestamp not null,
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {{ return(create_table_query) }}
{% endmacro %} 