{{
    config(
        materialized='incremental',
        unique_key=['year', 'month'],
        tags=['datamart', 'facts']
    )
}}

with monthly_order_facts as (
    select
        extract(year from order_date) as year,
        extract(month from order_date) as month,
        to_char(order_date, 'YYYY-MM') as year_month,
        count(distinct order_id) as orders_count,
        count(distinct customer_id) as unique_customers,
        sum(total_amount) as total_sales_amount,
        sum(shipping_cost) as total_shipping_cost,
        avg(total_amount) as average_order_value,
        sum(total_items) as total_items_sold,
        count(distinct case when status = 'completed' then order_id end) as completed_orders,
        count(distinct case when status = 'cancelled' then order_id end) as cancelled_orders
    from {{ ref('fct_orders') }}
    group by 1, 2, 3
),

monthly_product_category_sales as (
    select
        extract(year from order_date) as year,
        extract(month from order_date) as month,
        product_category,
        sum(item_total) as category_sales,
        count(distinct order_id) as category_orders,
        sum(quantity) as category_items_sold
    from {{ ref('fct_order_items') }}
    group by 1, 2, 3
),

monthly_new_customers as (
    select
        extract(year from first_order_date) as year,
        extract(month from first_order_date) as month,
        count(distinct customer_id) as new_customers
    from {{ ref('dim_customers') }}
    where first_order_date is not null
    group by 1, 2
)

select
    m.year,
    m.month,
    m.year_month,
    m.orders_count,
    m.unique_customers,
    m.total_sales_amount,
    m.total_shipping_cost,
    m.average_order_value,
    m.total_items_sold,
    m.completed_orders,
    m.cancelled_orders,
    coalesce(pc_electronics.category_sales, 0) as electronics_sales,
    coalesce(pc_clothing.category_sales, 0) as clothing_sales,
    coalesce(pc_footwear.category_sales, 0) as footwear_sales,
    coalesce(pc_accessories.category_sales, 0) as accessories_sales,
    coalesce(pc_electronics.category_items_sold, 0) as electronics_items_sold,
    coalesce(pc_clothing.category_items_sold, 0) as clothing_items_sold,
    coalesce(pc_footwear.category_items_sold, 0) as footwear_items_sold,
    coalesce(pc_accessories.category_items_sold, 0) as accessories_items_sold,
    coalesce(nc.new_customers, 0) as new_customers,
    case 
        when m.orders_count = 0 then 0
        else (m.cancelled_orders::float / m.orders_count) * 100
    end as cancellation_rate,
    case
        when lag(m.total_sales_amount) over (order by m.year, m.month) = 0 then null
        else (m.total_sales_amount - lag(m.total_sales_amount) over (order by m.year, m.month)) / 
             lag(m.total_sales_amount) over (order by m.year, m.month) * 100
    end as sales_growth_pct,
    current_timestamp as updated_at
from monthly_order_facts m
left join monthly_new_customers nc on m.year = nc.year and m.month = nc.month
left join monthly_product_category_sales pc_electronics 
    on m.year = pc_electronics.year and m.month = pc_electronics.month and pc_electronics.product_category = 'Electronics'
left join monthly_product_category_sales pc_clothing 
    on m.year = pc_clothing.year and m.month = pc_clothing.month and pc_clothing.product_category = 'Clothing'
left join monthly_product_category_sales pc_footwear 
    on m.year = pc_footwear.year and m.month = pc_footwear.month and pc_footwear.product_category = 'Footwear'
left join monthly_product_category_sales pc_accessories 
    on m.year = pc_accessories.year and m.month = pc_accessories.month and pc_accessories.product_category = 'Accessories'

{% if is_incremental() %}
where m.year || '-' || lpad(m.month::text, 2, '0') >= (select max(year || '-' || lpad(month::text, 2, '0')) from {{ this }})
{% endif %} 