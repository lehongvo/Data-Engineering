/*
  Custom test to verify that retention rates generally decrease over time
  for any given cohort. This is a typical pattern in retention analysis.
*/

with retention_rates as (
    select
        cohort,
        months_since_first_order,
        retention_rate,
        lead(retention_rate) over (
            partition by cohort
            order by months_since_first_order
        ) as next_month_retention_rate
    from {{ ref('metric_customer_retention') }}
    where months_since_first_order > 0
),

potential_issues as (
    select
        cohort,
        months_since_first_order,
        retention_rate,
        next_month_retention_rate,
        next_month_retention_rate - retention_rate as retention_rate_change
    from retention_rates
    where
        -- Check for months where retention rate increased by more than 20 percentage points
        -- Some increase can happen due to seasonality, delayed purchases, etc.
        -- but large unexpected increases should be investigated
        next_month_retention_rate is not null
        and next_month_retention_rate > retention_rate
        and (next_month_retention_rate - retention_rate) > 20
)

select * from potential_issues 