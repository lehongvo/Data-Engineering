{% macro calculate_growth_rate(value_column, partition_by=None, order_by=None) %}
    /*
    Calculates the period-over-period growth rate for a given value.
    
    Arguments:
        value_column: The column to calculate growth for
        partition_by: Optional partition expression (e.g., 'customer_id')
        order_by: Required order expression (e.g., 'date_day')
        
    Returns:
        A SQL expression for calculating growth rate as a percentage
    */
    
    {% if order_by is none %}
        {{ exceptions.raise_compiler_error("The order_by parameter is required for calculate_growth_rate") }}
    {% endif %}
    
    {% if partition_by is not none %}
        {% set window_spec = "partition by " ~ partition_by ~ " order by " ~ order_by %}
    {% else %}
        {% set window_spec = "order by " ~ order_by %}
    {% endif %}
    
    case
        when lag({{ value_column }}) over ({{ window_spec }}) is null 
            or lag({{ value_column }}) over ({{ window_spec }}) = 0
            then null
        else
            ({{ value_column }} - lag({{ value_column }}) over ({{ window_spec }})) / 
            nullif(lag({{ value_column }}) over ({{ window_spec }}), 0) * 100
    end

{% endmacro %} 