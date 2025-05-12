with products as (
    select * from "dbt_db"."public"."stg_products"
)

select
    product_id,
    name,
    price,
    category,
    created_at,
    current_timestamp as updated_at
from products