with source as (
    select * from "dbt_db"."public"."orders"
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