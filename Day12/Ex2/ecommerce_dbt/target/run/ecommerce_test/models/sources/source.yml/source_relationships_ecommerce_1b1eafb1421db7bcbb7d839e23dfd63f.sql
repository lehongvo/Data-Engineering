select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."source_relationships_ecommerce_1b1eafb1421db7bcbb7d839e23dfd63f"
    
      
    ) dbt_internal_test