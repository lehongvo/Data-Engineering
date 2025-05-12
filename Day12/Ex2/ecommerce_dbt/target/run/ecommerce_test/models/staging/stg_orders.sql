
  create view "dbt_db_ex2"."public"."stg_orders__dbt_tmp"
    
    
  as (
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
        'ea59a1a9-b4a6-48c7-85ca-a329413f07c8' as _invocation_id
    from source
)

select * from staged
  );