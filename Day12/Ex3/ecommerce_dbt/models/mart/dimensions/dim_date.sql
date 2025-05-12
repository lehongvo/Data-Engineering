{{
    config(
        materialized='table',
        tags=['datamart', 'dimensions']
    )
}}

-- Generate a date series from 2020-01-01 to 2025-12-31
with date_spine as (
    {{ dbt_utils.date_spine(
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2025-12-31' as date)",
        datepart="day"
    ) }}
),

dates as (
    select
        cast(date_day as date) as date_key,
        date_day,
        extract(year from date_day) as year,
        extract(month from date_day) as month,
        extract(day from date_day) as day_of_month,
        extract(quarter from date_day) as quarter,
        extract(week from date_day) as week_of_year,
        extract(dow from date_day) as day_of_week,
        extract(doy from date_day) as day_of_year,
        to_char(date_day, 'YYYY-MM') as year_month,
        to_char(date_day, 'Month') as month_name,
        to_char(date_day, 'Day') as day_name,
        case
            when extract(dow from date_day) in (0, 6) then true
            else false
        end as is_weekend,
        case
            when extract(month from date_day) in (1, 2, 3) then 'Q1'
            when extract(month from date_day) in (4, 5, 6) then 'Q2'
            when extract(month from date_day) in (7, 8, 9) then 'Q3'
            else 'Q4'
        end as quarter_name
    from date_spine
)

select * from dates 