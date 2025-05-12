
    
    

select
    date_key as unique_field,
    count(*) as n_records

from "dbt_db_ex3"."public"."metric_daily_sales"
where date_key is not null
group by date_key
having count(*) > 1


