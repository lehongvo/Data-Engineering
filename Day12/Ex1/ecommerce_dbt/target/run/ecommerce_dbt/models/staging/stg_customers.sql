
  create view "dbt_db"."public"."stg_customers__dbt_tmp"
    
    
  as (
    with source as (
    select * from "dbt_db"."public"."customers"
),

staged as (
    select
        customer_id,
        name,
        email,
        created_at
    from source
)

select * from staged
  );