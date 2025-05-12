
  
    

  create  table "dbt_db"."public"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    with customers as (
    select * from "dbt_db"."public"."stg_customers"
)

select
    customer_id,
    name,
    email,
    created_at,
    current_timestamp as updated_at
from customers
  );
  