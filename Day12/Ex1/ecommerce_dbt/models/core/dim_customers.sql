with customers as (
    select * from {{ ref('stg_customers') }}
)

select
    customer_id,
    name,
    email,
    created_at,
    current_timestamp as updated_at
from customers 