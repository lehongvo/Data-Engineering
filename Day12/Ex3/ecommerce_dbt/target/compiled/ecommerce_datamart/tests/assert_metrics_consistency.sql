/*
  Custom test to verify consistency between daily and monthly metrics aggregations.
  This test ensures the sum of daily metrics for a month matches the monthly metrics.
*/

with daily_metrics as (
    select
        extract(year from date_key) as year,
        extract(month from date_key) as month,
        sum(total_sales_amount) as daily_sum_sales,
        sum(orders_count) as daily_sum_orders,
        sum(customers_count) as daily_sum_customers
    from "dbt_db_ex3"."public"."metric_daily_sales"
    group by 1, 2
),

monthly_metrics as (
    select
        year,
        month,
        total_sales_amount as monthly_sales,
        orders_count as monthly_orders,
        unique_customers as monthly_customers
    from "dbt_db_ex3"."public"."metric_monthly_sales"
),

compared as (
    select
        d.year,
        d.month,
        d.daily_sum_sales,
        m.monthly_sales,
        abs(d.daily_sum_sales - m.monthly_sales) as sales_difference,
        d.daily_sum_orders,
        m.monthly_orders,
        abs(d.daily_sum_orders - m.monthly_orders) as orders_difference,
        d.daily_sum_customers,
        m.monthly_customers,
        abs(d.daily_sum_customers - m.monthly_customers) as customers_difference
    from daily_metrics d
    join monthly_metrics m 
        on d.year = m.year 
        and d.month = m.month
)

select * 
from compared 
where 
    sales_difference > 0.01 or -- Allow small rounding differences
    orders_difference > 0 or
    customers_difference > 0