{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

with source as (
    select * from {{ source('ecommerce_raw', 'orders') }}
    
    {% if is_incremental() %}
    where created_at >= (select max(created_at) from {{ this }})
    {% endif %}
),

staged as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        payment_method,
        shipping_address,
        shipping_cost,
        total_amount,
        created_at,
        updated_at
    from source
)

select * from staged 