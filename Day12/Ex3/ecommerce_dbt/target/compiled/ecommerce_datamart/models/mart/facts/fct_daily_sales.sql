

with order_facts as (
    select
        date_trunc('day', order_date) as order_day,
        count(distinct order_id) as orders_count,
        count(distinct customer_id) as customers_count,
        sum(total_amount) as total_sales_amount,
        sum(shipping_cost) as total_shipping_cost,
        sum(total_amount - shipping_cost) as total_product_revenue,
        avg(total_amount) as average_order_value,
        sum(total_items) as total_items_sold
    from "dbt_db_ex3"."public"."fct_orders"
    group by 1
),

product_category_facts as (
    select
        date_trunc('day', order_date) as order_day,
        product_category,
        count(distinct order_id) as category_orders_count,
        sum(item_total) as category_revenue,
        sum(quantity) as category_items_sold
    from "dbt_db_ex3"."public"."fct_order_items"
    group by 1, 2
)

select
    d.date_key,
    d.year,
    d.month,
    d.quarter,
    d.day_of_month,
    d.day_of_week,
    d.is_weekend,
    d.month_name,
    coalesce(o.orders_count, 0) as orders_count,
    coalesce(o.customers_count, 0) as customers_count,
    coalesce(o.total_sales_amount, 0) as total_sales_amount,
    coalesce(o.total_shipping_cost, 0) as total_shipping_cost,
    coalesce(o.total_product_revenue, 0) as total_product_revenue,
    coalesce(o.average_order_value, 0) as average_order_value,
    coalesce(o.total_items_sold, 0) as total_items_sold,
    -- Metrics specific to each product category
    coalesce(pc_electronics.category_revenue, 0) as electronics_revenue,
    coalesce(pc_clothing.category_revenue, 0) as clothing_revenue,
    coalesce(pc_footwear.category_revenue, 0) as footwear_revenue,
    coalesce(pc_accessories.category_revenue, 0) as accessories_revenue,
    -- Calculated metrics
    case 
        when coalesce(o.orders_count, 0) = 0 then 0
        else coalesce(o.customers_count, 0)::float / o.orders_count 
    end as customers_per_order_ratio,
    current_timestamp as updated_at
from "dbt_db_ex3"."public"."dim_date" d
left join order_facts o on d.date_key = o.order_day
left join product_category_facts pc_electronics 
    on d.date_key = pc_electronics.order_day and pc_electronics.product_category = 'Electronics'
left join product_category_facts pc_clothing 
    on d.date_key = pc_clothing.order_day and pc_clothing.product_category = 'Clothing'
left join product_category_facts pc_footwear 
    on d.date_key = pc_footwear.order_day and pc_footwear.product_category = 'Footwear'
left join product_category_facts pc_accessories 
    on d.date_key = pc_accessories.order_day and pc_accessories.product_category = 'Accessories'
where d.date_key <= current_date