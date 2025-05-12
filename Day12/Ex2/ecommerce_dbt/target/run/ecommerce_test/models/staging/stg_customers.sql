
  create view "dbt_db_ex2"."public"."stg_customers__dbt_tmp"
    
    
  as (
    with source as (
    select * from "dbt_db_ex2"."public"."customers"
),

staged as (
    select
        customer_id,
        name,
        trim(lower(email)) as email, -- Normalize email
        created_at
    from source
)

select * from staged
  );