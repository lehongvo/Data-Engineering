
  create view "dbt_db"."public"."stg_order_items__dbt_tmp"
    
    
  as (
    with source as (
    select * from "dbt_db"."public"."order_items"
),

staged as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        created_at
    from source
)

select * from staged
  );