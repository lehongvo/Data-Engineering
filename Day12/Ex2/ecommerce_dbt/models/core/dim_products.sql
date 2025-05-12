{{
    config(
        materialized='table',
        tags=['core', 'daily']
    )
}}

with products as (
    select * from {{ ref('stg_products') }}
),

product_sales as (
    select
        product_id,
        sum(quantity) as total_quantity_sold,
        sum(quantity * unit_price) as total_revenue
    from {{ ref('stg_order_items') }}
    group by 1
),

final as (
    select
        p.product_id,
        p.name,
        p.price,
        p.category,
        p.created_at,
        coalesce(ps.total_quantity_sold, 0) as total_quantity_sold,
        coalesce(ps.total_revenue, 0) as total_revenue,
        current_timestamp as updated_at
    from products p
    left join product_sales ps on p.product_id = ps.product_id
)

select * from final 