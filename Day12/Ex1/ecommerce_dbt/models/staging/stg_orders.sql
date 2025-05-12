with source as (
    select * from {{ source('ecommerce_raw', 'orders') }}
),

staged as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        created_at
    from source
)

select * from staged 