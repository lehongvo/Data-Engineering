
  
    

  create  table "dbt_db_ex3"."public"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    with customers as (
    select * from "dbt_db_ex3"."public"."stg_customers"
),

customer_orders as (
    select
        customer_id,
        count(*) as order_count,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        sum(total_amount) as lifetime_value
    from "dbt_db_ex3"."public"."stg_orders"
    group by 1
)

select
    c.customer_id,
    c.name,
    c.email,
    c.phone,
    c.created_at,
    coalesce(co.order_count, 0) as lifetime_orders,
    co.first_order_date,
    co.most_recent_order_date,
    coalesce(co.lifetime_value, 0) as lifetime_value,
    current_timestamp as updated_at
from customers c
left join customer_orders co using (customer_id)
  );
  