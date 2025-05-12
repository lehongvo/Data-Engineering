
    
    

with all_values as (

    select
        category as value_field,
        count(*) as n_records

    from "dbt_db_ex3"."public"."dim_products"
    group by category

)

select *
from all_values
where value_field not in (
    'Electronics','Clothing','Footwear','Accessories'
)


