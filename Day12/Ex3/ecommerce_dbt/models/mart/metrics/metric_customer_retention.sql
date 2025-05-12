{{
    config(
        materialized='table',
        tags=['datamart', 'metrics']
    )
}}

-- This is a materialized view that consolidates customer retention metrics
-- for easier analytics consumption

select
    first_order_year,
    first_order_month,
    cohort,
    cohort_size,
    months_since_first_order,
    retained_customers,
    cohort_revenue,
    retention_rate,
    revenue_per_retained_customer,
    cumulative_retained_customers,
    cumulative_cohort_revenue,
    -- Additional calculated metrics
    (cumulative_retained_customers::float / nullif(cohort_size, 0)) * 100 as cumulative_retention_rate,
    (cumulative_cohort_revenue::float / nullif(cumulative_retained_customers, 0)) as cumulative_revenue_per_customer,
    (retained_customers::float / nullif(lag(retained_customers) over (
        partition by cohort 
        order by months_since_first_order
    ), 0)) * 100 as month_over_month_retention_change,
    case
        when months_since_first_order >= 1 and months_since_first_order <= 3 then 'Early Stage'
        when months_since_first_order > 3 and months_since_first_order <= 6 then 'Mid Stage'
        when months_since_first_order > 6 and months_since_first_order <= 12 then 'Late Stage'
        else 'Long Term'
    end as retention_stage,
    current_timestamp as updated_at
from {{ ref('fct_customer_retention') }} 