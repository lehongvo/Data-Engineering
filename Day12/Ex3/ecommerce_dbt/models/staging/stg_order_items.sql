{{
    config(
        materialized='incremental',
        unique_key='order_item_id'
    )
}}

with source as (
    select * from {{ source('ecommerce_raw', 'order_items') }}
    
    {% if is_incremental() %}
    where created_at >= (select max(created_at) from {{ this }})
    {% endif %}
),

staged as (
    select
        order_item_id,
        order_id,
        product_id,
        greatest(quantity, 1) as quantity,
        coalesce(unit_price, 0) as unit_price,
        coalesce(discount_amount, 0) as discount_amount,
        (quantity * unit_price) - coalesce(discount_amount, 0) as item_total,
        created_at,
        updated_at
    from source
)

select * from staged 