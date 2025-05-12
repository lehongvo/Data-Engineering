select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."source_not_null_ecommerce_raw_customers_email"
    
      
    ) dbt_internal_test