with source as (
    select * from {{ source('ecommerce_raw', 'products') }}
),

staged as (
    select
        product_id,
        name,
        price,
        category,
        created_at
    from source
)

select * from staged 