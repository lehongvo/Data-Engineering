with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    o.customer_id,
    o.order_date,
    p.category as product_category,
    oi.quantity,
    oi.unit_price,
    oi.discount_amount,
    oi.item_total,
    (oi.unit_price * oi.quantity) as gross_item_sales_value,
    oi.discount_amount as item_discount_value,
    ((oi.unit_price * oi.quantity) - oi.item_total) as total_discount_impact,
    case
        when oi.discount_amount > 0 then true
        else false
    end as is_discounted,
    o.status as order_status,
    date_trunc('day', o.order_date) as order_day,
    date_trunc('week', o.order_date) as order_week,
    date_trunc('month', o.order_date) as order_month,
    oi.created_at,
    current_timestamp as updated_at
from order_items oi
join orders o using (order_id)
join products p using (product_id) 