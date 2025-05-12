/*
  Custom test to check if the total amount in orders table
  matches the sum of the item amounts in order_items.
  
  If there are differences, this test will return the records with discrepancies.
*/

with orders as (
    select 
        order_id,
        total_amount as order_total
    from "dbt_db_ex2"."public"."fct_orders"
),

order_items_grouped as (
    select
        order_id,
        sum(quantity * unit_price) as items_total
    from "dbt_db_ex2"."public"."stg_order_items"
    group by 1
),

joined as (
    select
        o.order_id,
        o.order_total,
        coalesce(oi.items_total, 0) as items_total,
        abs(o.order_total - coalesce(oi.items_total, 0)) as difference
    from orders o
    left join order_items_grouped oi on o.order_id = oi.order_id
)

select * from joined where difference > 0.01  -- Allow small rounding differences