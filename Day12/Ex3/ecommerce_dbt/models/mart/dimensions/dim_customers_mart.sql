{{
    config(
        materialized='table',
        tags=['datamart', 'dimensions']
    )
}}

with customers as (
    select * from {{ ref('dim_customers') }}
),

customer_segments as (
    select
        customer_id,
        case
            when lifetime_value >= 1000000 then 'VIP'
            when lifetime_value >= 500000 then 'High Value'
            when lifetime_value >= 100000 then 'Medium Value'
            else 'Low Value'
        end as customer_segment,
        case
            when lifetime_orders >= 10 then 'Frequent'
            when lifetime_orders >= 5 then 'Regular'
            when lifetime_orders >= 2 then 'Occasional'
            else 'One-time'
        end as purchase_frequency,
        case
            when datediff('day', most_recent_order_date, current_date) <= 30 then 'Active'
            when datediff('day', most_recent_order_date, current_date) <= 90 then 'Recent'
            when datediff('day', most_recent_order_date, current_date) <= 180 then 'Lapsed'
            else 'Inactive'
        end as customer_status
    from customers
    where lifetime_orders > 0
)

select
    c.*,
    coalesce(cs.customer_segment, 'New') as customer_segment,
    coalesce(cs.purchase_frequency, 'None') as purchase_frequency,
    coalesce(cs.customer_status, 'New') as customer_status,
    case
        when cs.customer_segment = 'VIP' and cs.customer_status = 'Active' then true
        else false
    end as is_high_value_active
from customers c
left join customer_segments cs using (customer_id) 