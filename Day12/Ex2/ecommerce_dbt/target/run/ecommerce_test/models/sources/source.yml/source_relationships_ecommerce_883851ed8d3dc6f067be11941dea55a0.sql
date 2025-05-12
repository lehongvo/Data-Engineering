select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."source_relationships_ecommerce_883851ed8d3dc6f067be11941dea55a0"
    
      
    ) dbt_internal_test