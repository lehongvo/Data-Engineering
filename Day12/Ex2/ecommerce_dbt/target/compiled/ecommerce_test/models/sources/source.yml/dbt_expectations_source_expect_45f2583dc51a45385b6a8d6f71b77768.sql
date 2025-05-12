




    with grouped_expression as (
    select
        
        
    
  


    

coalesce(array_length((select regexp_matches(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', '')), 1), 0)


 > 0
 as expression


    from "dbt_db_ex2"."public"."customers"
    

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




