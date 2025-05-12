select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex3"."public_dbt_test__audit"."unique_metric_daily_sales_date_key"
    
      
    ) dbt_internal_test