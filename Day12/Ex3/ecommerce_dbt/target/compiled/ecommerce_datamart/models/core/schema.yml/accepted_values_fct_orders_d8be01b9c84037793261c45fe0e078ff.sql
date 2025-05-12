
    
    

with all_values as (

    select
        status as value_field,
        count(*) as n_records

    from "dbt_db_ex3"."public"."fct_orders"
    group by status

)

select *
from all_values
where value_field not in (
    'completed','processing','cancelled','refunded'
)


