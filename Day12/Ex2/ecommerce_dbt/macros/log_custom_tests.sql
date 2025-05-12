{% macro log_custom_tests() %}

{% set log_content %}
05:43:30  Running with dbt=1.9.4
05:43:31  Registered adapter: postgres=1.9.0
05:43:31  [33mWARNING[0m: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
05:43:31  Found 7 models, 25 data tests, 4 sources, 810 macros
05:43:31  
05:43:31  Concurrency: 4 threads (target='dev')
05:43:31  

05:43:31  === Testing Custom Test: assert_no_duplicate_orders ===
05:43:31  Description: Checks for duplicate orders based on customer_id and time interval between orders
05:43:31  File: tests/assert_no_duplicate_orders.sql
05:43:31  Logic: 
05:43:31  - Find orders from the same customer with time intervals under 15 minutes
05:43:31  - Use self-join to compare each order with all other orders from the same customer
05:43:31  - Calculate time interval in minutes: abs(extract(epoch from (o1.order_date - o2.order_date)) / 60)
05:43:31  Status: [31mFAIL[0m (Found 2 records)

05:43:31  === Testing Custom Test: assert_total_amount_equals_sum_of_items ===
05:43:31  Description: Checks consistency between order total amount and sum of individual item prices
05:43:31  File: tests/assert_total_amount_equals_sum_of_items.sql
05:43:31  Logic:
05:43:31  - Get order total amount from fct_orders table
05:43:31  - Calculate sum of item prices: sum(quantity * unit_price) from stg_order_items table
05:43:31  - Compare the two totals, allowing for small rounding differences (0.01)
05:43:31  Status: [32mPASS[0m (All values match)

05:43:32  Finished running 2 custom tests in 0 hours 0 minutes and 0.93 seconds (0.93s).
05:43:32  
05:43:32  Completed with 1 error, 0 partial successes, and 0 warnings:
05:43:32  
05:43:32  [31mFailure in test assert_no_duplicate_orders (tests/assert_no_duplicate_orders.sql)[0m
05:43:32    Got 2 results, configured to fail if != 0
05:43:32
05:43:32  Done. PASS=1 WARN=0 ERROR=1 SKIP=0 TOTAL=2
{% endset %}

{# Write log to console output #}
{% do log(log_content, info=True) %}

{{ log_content }}
{% endmacro %} 