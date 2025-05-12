{{
    config(
        materialized='table',
        tags=['core', 'daily']
    )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

customer_orders as (
    select
        customer_id,
        count(*) as lifetime_orders,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date
    from {{ ref('stg_orders') }}
    group by 1
),

final as (
    select
        c.customer_id,
        c.name,
        c.email,
        c.created_at,
        coalesce(co.lifetime_orders, 0) as lifetime_orders,
        co.first_order_date,
        co.most_recent_order_date,
        current_timestamp as updated_at
    from customers c
    left join customer_orders co on c.customer_id = co.customer_id
)

select * from final 