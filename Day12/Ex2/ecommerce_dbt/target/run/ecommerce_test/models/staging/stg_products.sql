
  create view "dbt_db_ex2"."public"."stg_products__dbt_tmp"
    
    
  as (
    with source as (
    select * from "dbt_db_ex2"."public"."products"
),

staged as (
    select
        product_id,
        name,
        coalesce(price, 0) as price, -- Ensure no NULL values
        category,
        created_at
    from source
)

select * from staged
  );