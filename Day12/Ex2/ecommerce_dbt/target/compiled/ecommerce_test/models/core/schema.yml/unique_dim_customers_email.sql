
    
    

select
    email as unique_field,
    count(*) as n_records

from "dbt_db_ex2"."public"."dim_customers"
where email is not null
group by email
having count(*) > 1


