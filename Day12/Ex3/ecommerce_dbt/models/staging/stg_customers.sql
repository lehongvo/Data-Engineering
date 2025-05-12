with source as (
    select * from {{ source('ecommerce_raw', 'customers') }}
),

staged as (
    select
        customer_id,
        name,
        trim(lower(email)) as email,
        coalesce(phone, 'Unknown') as phone,
        created_at,
        updated_at
    from source
)

select * from staged 