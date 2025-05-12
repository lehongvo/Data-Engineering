select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex3"."public_dbt_test__audit"."not_null_dim_customers_lifetime_orders"
    
      
    ) dbt_internal_test