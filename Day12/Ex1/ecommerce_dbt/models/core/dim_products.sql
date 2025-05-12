with products as (
    select * from {{ ref('stg_products') }}
)

select
    product_id,
    name,
    price,
    category,
    created_at,
    current_timestamp as updated_at
from products 