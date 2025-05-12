/*
  Custom test to ensure there are no duplicate orders in the core table.
  This test checks for duplicates based on customer_id and order_date within 15 minutes
*/

with orders as (
    select 
        customer_id,
        order_date,
        count(*) as order_count
    from {{ ref('stg_orders') }}
    group by 1, 2
),

potential_duplicates as (
    select
        o1.customer_id,
        o1.order_date as order_date_1,
        o2.order_date as order_date_2,
        abs(extract(epoch from (o1.order_date - o2.order_date)) / 60) as minutes_difference
    from {{ ref('stg_orders') }} o1
    join {{ ref('stg_orders') }} o2
        on o1.customer_id = o2.customer_id
        and o1.order_id <> o2.order_id
        and abs(extract(epoch from (o1.order_date - o2.order_date)) / 60) < 15  -- Orders less than 15 minutes apart
)

select * from potential_duplicates 