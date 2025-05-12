with source as (
    select * from "dbt_db"."public"."customers"
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