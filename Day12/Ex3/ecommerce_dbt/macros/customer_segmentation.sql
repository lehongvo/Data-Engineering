{% macro customer_segmentation(value_column, segment_boundaries, segment_names) %}
    /*
    Creates a CASE statement for customer segmentation based on a value column.
    
    Arguments:
        value_column: The column to use for segmentation
        segment_boundaries: List of boundary values in ascending order
        segment_names: List of segment names (length should be len(segment_boundaries) + 1)
        
    Returns:
        A SQL CASE expression that segments customers based on the given value
    */
    
    {% if segment_boundaries|length != segment_names|length - 1 %}
        {{ exceptions.raise_compiler_error("segment_names should have one more element than segment_boundaries") }}
    {% endif %}
    
    case
        {% for boundary in segment_boundaries %}
            {% set i = loop.index0 %}
            when {{ value_column }} < {{ boundary }} then '{{ segment_names[i] }}'
        {% endfor %}
        else '{{ segment_names[-1] }}'
    end

{% endmacro %} 