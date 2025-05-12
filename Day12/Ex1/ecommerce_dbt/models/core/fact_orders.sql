with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_with_items as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        o.status,
        sum(oi.quantity * oi.unit_price) as total_amount,
        count(oi.order_item_id) as total_items
    from orders o
    left join order_items oi on o.order_id = oi.order_id
    group by 1, 2, 3, 4
)

select
    order_id,
    customer_id,
    order_date,
    status,
    total_amount,
    total_items,
    current_timestamp as updated_at
from order_with_items 