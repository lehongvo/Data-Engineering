select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."accepted_values_dim_products_d7178e429849cd46479b7235b8b9a680"
    
      
    ) dbt_internal_test