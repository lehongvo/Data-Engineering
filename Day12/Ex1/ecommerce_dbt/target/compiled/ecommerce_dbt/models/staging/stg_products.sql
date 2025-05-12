with source as (
    select * from "dbt_db"."public"."products"
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