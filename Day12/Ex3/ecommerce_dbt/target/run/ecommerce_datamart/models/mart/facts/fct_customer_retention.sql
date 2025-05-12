
  
    

  create  table "dbt_db_ex3"."public"."fct_customer_retention__dbt_tmp"
  
  
    as
  
  (
    

with customer_orders as (
    select
        customer_id,
        order_id,
        order_date,
        total_amount,
        row_number() over(partition by customer_id order by order_date) as order_sequence,
        lead(order_date) over(partition by customer_id order by order_date) as next_order_date,
        extract(day from (lead(order_date) over(partition by customer_id order by order_date) - order_date)) as days_until_next_order
    from "dbt_db_ex3"."public"."fct_orders"
),

customer_first_orders as (
    select
        customer_id,
        min(case when order_sequence = 1 then order_date end) as first_order_date,
        extract(year from min(case when order_sequence = 1 then order_date end)) as first_order_year,
        extract(month from min(case when order_sequence = 1 then order_date end)) as first_order_month,
        to_char(min(case when order_sequence = 1 then order_date end), 'YYYY-MM') as first_order_year_month
    from customer_orders
    group by 1
),

repeat_purchase_facts as (
    select
        c.customer_id,
        c.first_order_date,
        c.first_order_year,
        c.first_order_month,
        c.first_order_year_month,
        count(distinct case when co.order_sequence > 1 then co.order_id end) as repeat_orders,
        max(co.order_sequence) as total_orders,
        sum(case when co.order_sequence > 1 then co.total_amount else 0 end) as repeat_order_revenue,
        min(case when co.order_sequence = 2 then co.order_date end) as second_order_date,
        avg(co.days_until_next_order) as avg_days_between_orders
    from customer_first_orders c
    left join customer_orders co using (customer_id)
    group by 1, 2, 3, 4, 5
),

cohort_sizes as (
    select
        first_order_year,
        first_order_month,
        first_order_year_month,
        count(distinct customer_id) as cohort_size
    from customer_first_orders
    group by 1, 2, 3
),

retention_by_month as (
    select
        c.first_order_year,
        c.first_order_month,
        c.first_order_year_month,
        cs.cohort_size,
        date_part('month', age(date_trunc('month', o.order_date), 
                              date_trunc('month', c.first_order_date))) as months_since_first_order,
        count(distinct o.customer_id) as retained_customers,
        sum(o.total_amount) as cohort_revenue
    from customer_first_orders c
    join "dbt_db_ex3"."public"."fct_orders" o using(customer_id)
    join cohort_sizes cs 
        on c.first_order_year = cs.first_order_year 
        and c.first_order_month = cs.first_order_month
    where o.order_date > c.first_order_date
    group by 1, 2, 3, 4, 5
)

select
    r.first_order_year,
    r.first_order_month,
    r.first_order_year_month as cohort,
    r.cohort_size,
    r.months_since_first_order,
    r.retained_customers,
    r.cohort_revenue,
    (r.retained_customers::float / r.cohort_size) * 100 as retention_rate,
    (r.cohort_revenue::float / r.retained_customers) as revenue_per_retained_customer,
    sum(r.retained_customers) over (
        partition by r.first_order_year, r.first_order_month
        order by r.months_since_first_order
        rows between unbounded preceding and current row
    ) as cumulative_retained_customers,
    sum(r.cohort_revenue) over (
        partition by r.first_order_year, r.first_order_month
        order by r.months_since_first_order
        rows between unbounded preceding and current row
    ) as cumulative_cohort_revenue,
    current_timestamp as updated_at
from retention_by_month r
order by r.first_order_year, r.first_order_month, r.months_since_first_order
  );
  