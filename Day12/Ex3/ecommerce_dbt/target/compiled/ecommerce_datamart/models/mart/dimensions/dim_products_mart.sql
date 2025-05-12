

with products as (
    select * from "dbt_db_ex3"."public"."dim_products"
)

select
    p.*,
    case
        when total_quantity_sold > 100 then 'High Selling'
        when total_quantity_sold > 50 then 'Medium Selling'
        when total_quantity_sold > 0 then 'Low Selling'
        else 'Not Selling'
    end as sales_performance,
    case
        when total_revenue > 10000000 then 'High Revenue'
        when total_revenue > 5000000 then 'Medium Revenue'
        when total_revenue > 0 then 'Low Revenue'
        else 'No Revenue'
    end as revenue_tier,
    (total_revenue / nullif(total_quantity_sold, 0)) as average_selling_price,
    case
        when is_active = true and inventory_status != 'Out of stock' then true
        else false
    end as is_available_for_purchase,
    case
        when is_active = false then 'Discontinued'
        when inventory_status = 'Out of stock' then 'Temporarily Unavailable'
        else 'Available'
    end as availability_status
from products p