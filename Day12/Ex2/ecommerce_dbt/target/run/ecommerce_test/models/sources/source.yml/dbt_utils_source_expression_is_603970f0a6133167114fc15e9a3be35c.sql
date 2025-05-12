select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."dbt_utils_source_expression_is_603970f0a6133167114fc15e9a3be35c"
    
      
    ) dbt_internal_test