{% macro test_not_negative(model, column_name) %}

with validation as (
    select
        {{ column_name }} as field_to_check
    from {{ model }}
),

validation_errors as (
    select
        field_to_check
    from validation
    where field_to_check < 0
)

select * from validation_errors

{% endmacro %}


{% macro test_date_in_range(model, column_name, min_date, max_date) %}

{% set min_date_str = "'" ~ min_date ~ "'" %}
{% set max_date_str = "'" ~ max_date ~ "'" if max_date else 'current_date' %}

with validation as (
    select
        {{ column_name }} as date_field
    from {{ model }}
),

validation_errors as (
    select
        date_field
    from validation
    where date_field < {{ min_date_str }}
    {% if max_date %}
        or date_field > {{ max_date_str }}
    {% endif %}
)

select * from validation_errors

{% endmacro %} 