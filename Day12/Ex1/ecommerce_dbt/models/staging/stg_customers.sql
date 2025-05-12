with source as (
    select * from {{ source('ecommerce_raw', 'customers') }}
),

staged as (
    select
        customer_id,
        name,
        email,
        created_at
    from source
)

select * from staged 