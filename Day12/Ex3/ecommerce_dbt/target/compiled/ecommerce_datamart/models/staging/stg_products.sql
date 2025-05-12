with source as (
    select * from "dbt_db_ex3"."public"."products"
),

staged as (
    select
        product_id,
        name,
        coalesce(price, 0) as price,
        category,
        coalesce(inventory_count, 0) as inventory_count,
        is_active,
        created_at,
        updated_at
    from source
)

select * from staged