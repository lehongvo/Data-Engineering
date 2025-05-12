{% macro monitor_db_performance() %}
  /*
  Collects database performance metrics including:
  - Table sizes
  - Index usage
  - Long-running queries
  - Vacuum status
  - Connection counts
  
  This should be run after a dbt job completes to collect performance metrics.
  */
  
  {# Monitor table sizes #}
  {% set table_size_query %}
    select 
      nspname as schema_name,
      relname as table_name,
      pg_size_pretty(pg_total_relation_size(C.oid)) as total_size,
      pg_size_pretty(pg_relation_size(C.oid)) as table_size,
      pg_size_pretty(pg_total_relation_size(C.oid) - pg_relation_size(C.oid)) as index_size,
      pg_total_relation_size(C.oid) as total_bytes
    from pg_class C
    left join pg_namespace N on (N.oid = C.relnamespace)
    where nspname = '{{ target.schema }}'
      and C.relkind = 'r'
    order by pg_total_relation_size(C.oid) desc
    limit 20
  {% endset %}
  
  {% set table_sizes = run_query(table_size_query) %}
  
  {% set table_size_log_query %}
    create table if not exists {{ target.schema }}.table_size_log (
      id serial primary key,
      schema_name varchar(100) not null,
      table_name varchar(100) not null,
      total_size varchar(100) not null,
      table_size varchar(100) not null,
      index_size varchar(100) not null,
      total_bytes bigint not null,
      run_id varchar(100) not null,
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(table_size_log_query) %}
  
  {% for row in table_sizes %}
    {% set insert_size_log %}
      insert into {{ target.schema }}.table_size_log (
        schema_name,
        table_name,
        total_size,
        table_size,
        index_size,
        total_bytes,
        run_id
      ) values (
        '{{ row[0] }}',
        '{{ row[1] }}',
        '{{ row[2] }}',
        '{{ row[3] }}',
        '{{ row[4] }}',
        {{ row[5] }},
        '{{ run_id }}'
      )
    {% endset %}
    
    {% do run_query(insert_size_log) %}
  {% endfor %}
  
  {# Monitor index usage #}
  {% set index_usage_query %}
    select
      schemaname as schema_name,
      relname as table_name,
      indexrelname as index_name,
      idx_scan as index_scans,
      idx_tup_read as tuples_read,
      idx_tup_fetch as tuples_fetched
    from pg_stat_user_indexes
    where schemaname = '{{ target.schema }}'
    order by idx_scan desc
    limit 20
  {% endset %}
  
  {% set index_usage = run_query(index_usage_query) %}
  
  {% set index_usage_log_query %}
    create table if not exists {{ target.schema }}.index_usage_log (
      id serial primary key,
      schema_name varchar(100) not null,
      table_name varchar(100) not null,
      index_name varchar(100) not null,
      index_scans bigint not null,
      tuples_read bigint not null,
      tuples_fetched bigint not null,
      run_id varchar(100) not null,
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(index_usage_log_query) %}
  
  {% for row in index_usage %}
    {% set insert_index_log %}
      insert into {{ target.schema }}.index_usage_log (
        schema_name,
        table_name,
        index_name,
        index_scans,
        tuples_read,
        tuples_fetched,
        run_id
      ) values (
        '{{ row[0] }}',
        '{{ row[1] }}',
        '{{ row[2] }}',
        {{ row[3] }},
        {{ row[4] }},
        {{ row[5] }},
        '{{ run_id }}'
      )
    {% endset %}
    
    {% do run_query(insert_index_log) %}
  {% endfor %}
  
  {# Monitor vacuum status #}
  {% set vacuum_stats_query %}
    select
      schemaname as schema_name,
      relname as table_name,
      last_vacuum,
      last_autovacuum,
      vacuum_count,
      autovacuum_count,
      n_dead_tup as dead_tuples,
      n_live_tup as live_tuples,
      (n_dead_tup::float / nullif(n_live_tup, 0)) * 100 as dead_tuples_pct
    from pg_stat_user_tables
    where schemaname = '{{ target.schema }}'
    order by n_dead_tup desc
    limit 20
  {% endset %}
  
  {% set vacuum_stats = run_query(vacuum_stats_query) %}
  
  {% set vacuum_stats_log_query %}
    create table if not exists {{ target.schema }}.vacuum_stats_log (
      id serial primary key,
      schema_name varchar(100) not null,
      table_name varchar(100) not null,
      last_vacuum timestamp,
      last_autovacuum timestamp,
      vacuum_count bigint,
      autovacuum_count bigint,
      dead_tuples bigint,
      live_tuples bigint,
      dead_tuples_pct float,
      run_id varchar(100) not null,
      logged_at timestamp default current_timestamp
    )
  {% endset %}
  
  {% do run_query(vacuum_stats_log_query) %}
  
  {% for row in vacuum_stats %}
    {% set insert_vacuum_log %}
      insert into {{ target.schema }}.vacuum_stats_log (
        schema_name,
        table_name,
        last_vacuum,
        last_autovacuum,
        vacuum_count,
        autovacuum_count,
        dead_tuples,
        live_tuples,
        dead_tuples_pct,
        run_id
      ) values (
        '{{ row[0] }}',
        '{{ row[1] }}',
        {{ "'" ~ row[2] ~ "'" if row[2] else 'null' }},
        {{ "'" ~ row[3] ~ "'" if row[3] else 'null' }},
        {{ row[4] }},
        {{ row[5] }},
        {{ row[6] }},
        {{ row[7] }},
        {{ row[8] if row[8] else 'null' }},
        '{{ run_id }}'
      )
    {% endset %}
    
    {% do run_query(insert_vacuum_log) %}
  {% endfor %}
  
  {# Generate reports #}
  {% set report_content %}
Database Performance Report: {{ modules.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") }}
Run ID: {{ run_id }}

TOP 10 LARGEST TABLES:
{% for row in table_sizes if loop.index <= 10 %}
{{ row[1] }} ({{ row[2] }}) - Table: {{ row[3] }}, Indexes: {{ row[4] }}
{% endfor %}

TOP 10 MOST USED INDEXES:
{% for row in index_usage if loop.index <= 10 %}
{{ row[2] }} ({{ row[1] }}) - Scans: {{ row[3] }}
{% endfor %}

TABLES NEEDING VACUUM:
{% for row in vacuum_stats if row[8] and row[8] > 20 %}
{{ row[1] }} - Dead tuples: {{ row[6] }} ({{ row[8]|round(2) }}%)
{% endfor %}
  {% endset %}
  
  {% do log_to_file(
    file_path="../../reports/performance/db_performance_" ~ modules.datetime.datetime.now().strftime("%Y%m%d") ~ ".log",
    content=report_content
  ) %}
  
  {{ return('') }}
{% endmacro %}