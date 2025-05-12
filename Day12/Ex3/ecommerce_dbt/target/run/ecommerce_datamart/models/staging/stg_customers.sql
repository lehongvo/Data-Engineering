
  create view "dbt_db_ex3"."public"."stg_customers__dbt_tmp"
    
    
  as (
    with source as (
    select * from "dbt_db_ex3"."public"."customers"
),

staged as (
    select
        customer_id,
        name,
        trim(lower(email)) as email,
        coalesce(phone, 'Unknown') as phone,
        created_at,
        updated_at
    from source
)

select * from staged
  );