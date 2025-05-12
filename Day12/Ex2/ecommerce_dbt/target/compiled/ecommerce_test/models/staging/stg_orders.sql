with source as (
    select * from "dbt_db_ex2"."public"."orders"
),

staged as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        created_at,
        -- Add tracking for data lineage
        '5bc188b1-e30b-470c-9905-f7e712bfd576' as _invocation_id
    from source
)

select * from staged