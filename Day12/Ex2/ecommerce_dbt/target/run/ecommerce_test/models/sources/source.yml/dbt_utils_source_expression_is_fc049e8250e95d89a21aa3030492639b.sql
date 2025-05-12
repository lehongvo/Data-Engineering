select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."dbt_utils_source_expression_is_fc049e8250e95d89a21aa3030492639b"
    
      
    ) dbt_internal_test