

with source as (
    select * from "dbt_db_ex3"."public"."orders"
    
    
    where created_at >= (select max(created_at) from "dbt_db_ex3"."public"."stg_orders")
    
),

staged as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        payment_method,
        shipping_address,
        shipping_cost,
        total_amount,
        created_at,
        updated_at
    from source
)

select * from staged