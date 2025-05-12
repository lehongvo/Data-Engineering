select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."dbt_utils_source_expression_is_153dfd9cd11a491818a4174d0cdc2f9b"
    
      
    ) dbt_internal_test