




    with grouped_expression as (
    select
        
        
    
  


    

coalesce(array_length((select regexp_matches(email, '^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', '')), 1), 0)


 > 0
 as expression


    from "dbt_db_ex2"."public"."dim_customers"
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors




