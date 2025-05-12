with source as (
    select * from {{ source('ecommerce_raw', 'order_items') }}
),

staged as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        created_at
    from source
)

select * from staged 