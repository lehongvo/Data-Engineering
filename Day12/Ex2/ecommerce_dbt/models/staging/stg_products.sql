with source as (
    select * from {{ source('ecommerce_raw', 'products') }}
),

staged as (
    select
        product_id,
        name,
        coalesce(price, 0) as price, -- Ensure no NULL values
        category,
        created_at
    from source
)

select * from staged 