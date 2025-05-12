select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."dbt_expectations_source_expect_45f2583dc51a45385b6a8d6f71b77768"
    
      
    ) dbt_internal_test