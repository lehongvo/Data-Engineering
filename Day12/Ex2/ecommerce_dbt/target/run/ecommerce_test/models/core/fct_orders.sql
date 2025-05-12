
  
    

  create  table "dbt_db_ex2"."public"."fct_orders__dbt_tmp"
  
  
    as
  
  (
    

with orders as (
    select * from "dbt_db_ex2"."public"."stg_orders"
),

order_items as (
    select * from "dbt_db_ex2"."public"."stg_order_items"
),

order_totals as (
    select
        order_id,
        sum(quantity) as total_items,
        sum(quantity * unit_price) as total_amount
    from order_items
    group by 1
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        o.status,
        coalesce(ot.total_items, 0) as total_items,
        coalesce(ot.total_amount, 0) as total_amount,
        o.created_at,
        current_timestamp as updated_at,
        o._invocation_id
    from orders o
    left join order_totals ot on o.order_id = ot.order_id
)

select * from final
  );
  