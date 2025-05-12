
  create view "dbt_db_ex2"."public"."stg_order_items__dbt_tmp"
    
    
  as (
    with source as (
    select * from "dbt_db_ex2"."public"."order_items"
),

staged as (
    select
        order_item_id,
        order_id,
        product_id,
        greatest(quantity, 1) as quantity, -- Ensure minimum quantity is 1
        coalesce(unit_price, 0) as unit_price, -- Ensure no NULL prices
        created_at
    from source
)

select * from staged
  );