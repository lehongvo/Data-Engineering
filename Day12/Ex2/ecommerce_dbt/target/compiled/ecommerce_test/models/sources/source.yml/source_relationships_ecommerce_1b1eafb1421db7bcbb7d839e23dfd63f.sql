
    
    

with child as (
    select order_id as from_field
    from "dbt_db_ex2"."public"."order_items"
    where order_id is not null
),

parent as (
    select order_id as to_field
    from "dbt_db_ex2"."public"."orders"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


