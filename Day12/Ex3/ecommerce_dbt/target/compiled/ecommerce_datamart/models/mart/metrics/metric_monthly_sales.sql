

-- This is a materialized view that consolidates monthly sales metrics
-- for easier analytics consumption

select
    year,
    month,
    year_month,
    orders_count,
    unique_customers,
    total_sales_amount,
    total_shipping_cost,
    average_order_value,
    total_items_sold,
    completed_orders,
    cancelled_orders,
    electronics_sales,
    clothing_sales,
    footwear_sales,
    accessories_sales,
    electronics_items_sold,
    clothing_items_sold,
    footwear_items_sold,
    accessories_items_sold,
    new_customers,
    cancellation_rate,
    sales_growth_pct,
    -- Additional calculated metrics
    case
        when lag(new_customers) over (order by year, month) = 0 then null
        else (new_customers - lag(new_customers) over (order by year, month)) / 
             nullif(lag(new_customers) over (order by year, month), 0) * 100
    end as new_customer_growth_pct,
    case 
        when unique_customers = 0 then 0 
        else total_sales_amount / unique_customers 
    end as revenue_per_customer,
    (completed_orders::float / nullif(orders_count, 0)) * 100 as completion_rate,
    case
        when total_sales_amount = 0 then 0
        else electronics_sales / total_sales_amount * 100
    end as electronics_sales_pct,
    case
        when total_sales_amount = 0 then 0
        else clothing_sales / total_sales_amount * 100
    end as clothing_sales_pct,
    case
        when total_sales_amount = 0 then 0
        else footwear_sales / total_sales_amount * 100
    end as footwear_sales_pct,
    case
        when total_sales_amount = 0 then 0
        else accessories_sales / total_sales_amount * 100
    end as accessories_sales_pct,
    current_timestamp as updated_at
from "dbt_db_ex3"."public"."fct_monthly_sales"