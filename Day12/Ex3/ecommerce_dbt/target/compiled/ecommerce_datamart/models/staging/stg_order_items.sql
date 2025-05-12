

with source as (
    select * from "dbt_db_ex3"."public"."order_items"
    
    
    where created_at >= (select max(created_at) from "dbt_db_ex3"."public"."stg_order_items")
    
),

staged as (
    select
        order_item_id,
        order_id,
        product_id,
        greatest(quantity, 1) as quantity,
        coalesce(unit_price, 0) as unit_price,
        coalesce(discount_amount, 0) as discount_amount,
        (quantity * unit_price) - coalesce(discount_amount, 0) as item_total,
        created_at,
        updated_at
    from source
)

select * from staged