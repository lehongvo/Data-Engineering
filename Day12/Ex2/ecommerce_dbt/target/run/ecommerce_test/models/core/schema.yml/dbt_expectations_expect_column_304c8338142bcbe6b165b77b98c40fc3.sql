select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."dbt_expectations_expect_column_304c8338142bcbe6b165b77b98c40fc3"
    
      
    ) dbt_internal_test