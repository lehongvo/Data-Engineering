
  create view "dbt_db"."public"."stg_products__dbt_tmp"
    
    
  as (
    with source as (
    select * from "dbt_db"."public"."products"
),

staged as (
    select
        product_id,
        name,
        price,
        category,
        created_at
    from source
)

select * from staged
  );