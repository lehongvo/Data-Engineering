with source as (
    select * from {{ source('ecommerce_raw', 'order_items') }}
),

staged as (
    select
        order_item_id,
        order_id,
        product_id,
        greatest(quantity, 1) as quantity, -- Ensure minimum quantity is 1
        coalesce(unit_price, 0) as unit_price, -- Ensure no NULL prices
        created_at
    from source
)

select * from staged 