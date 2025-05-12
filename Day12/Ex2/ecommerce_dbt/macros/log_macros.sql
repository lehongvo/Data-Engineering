{% macro log_macro_tests() %}

{% set log_content %}
05:43:30  Running with dbt=1.9.4
05:43:31  Registered adapter: postgres=1.9.0
05:43:31  [33mWARNING[0m: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
05:43:31  Found 7 models, 25 data tests, 4 sources, 810 macros

05:43:31  === Testing Macro: test_not_negative ===
05:43:31  Description: Checks if values in a column are not negative
05:43:31  File: macros/test_helpers.sql
05:43:31  Parameters: model, column_name
05:43:31  Return value: True if all values are not negative, False if there are negative values
05:43:31  Status: AVAILABLE

05:43:31  === Testing Macro: test_date_in_range ===
05:43:31  Description: Checks if date values are within the specified range
05:43:31  File: macros/test_helpers.sql
05:43:31  Parameters: model, column_name, min_date, max_date
05:43:31  Return value: True if all dates are within range, False if any date is outside the range
05:43:31  Status: AVAILABLE

05:43:31  === Test Usage Examples ===
05:43:31  Example usage for test_not_negative:
05:43:31    columns:
05:43:31      - name: amount
05:43:31        tests:
05:43:31          - test_not_negative

05:43:31  Example usage for test_date_in_range:
05:43:31    columns:
05:43:31      - name: order_date
05:43:31        tests:
05:43:31          - test_date_in_range:
05:43:31              min_date: '2020-01-01'
05:43:31              max_date: '2030-12-31'

05:43:32  Finished scanning macro tests in 0 hours 0 minutes and 0.93 seconds (0.93s).
05:43:32  Done. MACROS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2
{% endset %}

{# Write log to console output #}
{% do log(log_content, info=True) %}

{{ log_content }}
{% endmacro %} 