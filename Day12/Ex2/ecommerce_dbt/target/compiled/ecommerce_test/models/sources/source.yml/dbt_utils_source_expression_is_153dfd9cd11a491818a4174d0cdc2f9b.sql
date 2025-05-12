



select
    *
from "dbt_db_ex2"."public"."order_items"

where not(quantity > 0)

