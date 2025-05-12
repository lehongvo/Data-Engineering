with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select
        order_id,
        count(*) as number_of_items,
        sum(quantity) as total_items,
        sum(item_total) as items_subtotal
    from {{ ref('stg_order_items') }}
    group by 1
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.payment_method,
    o.shipping_address,
    o.shipping_cost,
    o.total_amount,
    oi.number_of_items,
    oi.total_items,
    oi.items_subtotal,
    (oi.items_subtotal + o.shipping_cost) as calculated_total,
    abs(o.total_amount - (oi.items_subtotal + o.shipping_cost)) as total_amount_discrepancy,
    o.created_at,
    o.updated_at,
    date_trunc('day', o.order_date) as order_day,
    date_trunc('week', o.order_date) as order_week,
    date_trunc('month', o.order_date) as order_month,
    extract(hour from o.order_date) as order_hour
from orders o
left join order_items oi using (order_id) 