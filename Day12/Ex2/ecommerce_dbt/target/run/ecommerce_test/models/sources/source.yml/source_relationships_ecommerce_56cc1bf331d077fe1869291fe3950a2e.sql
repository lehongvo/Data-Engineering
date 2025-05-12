select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."source_relationships_ecommerce_56cc1bf331d077fe1869291fe3950a2e"
    
      
    ) dbt_internal_test