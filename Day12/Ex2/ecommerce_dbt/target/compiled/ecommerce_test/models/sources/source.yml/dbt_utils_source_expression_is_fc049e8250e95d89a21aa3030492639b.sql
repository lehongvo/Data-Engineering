



select
    *
from "dbt_db_ex2"."public"."products"

where not(price >= 0)

