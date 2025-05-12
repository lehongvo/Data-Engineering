
  
    

  create  table "dbt_db_ex3"."public"."dim_products__dbt_tmp"
  
  
    as
  
  (
    with products as (
    select * from "dbt_db_ex3"."public"."stg_products"
),

product_sales as (
    select
        product_id,
        sum(quantity) as total_quantity_sold,
        sum(item_total) as total_revenue
    from "dbt_db_ex3"."public"."stg_order_items"
    group by 1
)

select
    p.product_id,
    p.name,
    p.price,
    p.category,
    p.inventory_count,
    p.is_active,
    p.created_at,
    coalesce(ps.total_quantity_sold, 0) as total_quantity_sold,
    coalesce(ps.total_revenue, 0) as total_revenue,
    case
        when p.inventory_count = 0 then 'Out of stock'
        when p.inventory_count < 10 then 'Low stock'
        else 'In stock'
    end as inventory_status,
    current_timestamp as updated_at
from products p
left join product_sales ps using (product_id)
  );
  