

-- This is a materialized view that consolidates daily sales metrics
-- for easier analytics consumption

select
    date_key,
    year,
    month,
    quarter,
    day_of_month,
    day_of_week,
    is_weekend,
    month_name,
    orders_count,
    customers_count,
    total_sales_amount,
    total_shipping_cost,
    total_product_revenue,
    average_order_value,
    total_items_sold,
    electronics_revenue,
    clothing_revenue,
    footwear_revenue,
    accessories_revenue,
    -- Additional calculated metrics
    case 
        when orders_count = 0 then 0 
        else total_sales_amount / orders_count 
    end as revenue_per_order,
    case 
        when customers_count = 0 then 0 
        else total_sales_amount / customers_count 
    end as revenue_per_customer,
    case 
        when total_sales_amount = 0 then 0 
        else electronics_revenue / total_sales_amount * 100 
    end as electronics_revenue_pct,
    case 
        when total_sales_amount = 0 then 0 
        else clothing_revenue / total_sales_amount * 100 
    end as clothing_revenue_pct,
    case 
        when total_sales_amount = 0 then 0 
        else footwear_revenue / total_sales_amount * 100 
    end as footwear_revenue_pct,
    case 
        when total_sales_amount = 0 then 0 
        else accessories_revenue / total_sales_amount * 100 
    end as accessories_revenue_pct,
    current_timestamp as updated_at
from "dbt_db_ex3"."public"."fct_daily_sales"