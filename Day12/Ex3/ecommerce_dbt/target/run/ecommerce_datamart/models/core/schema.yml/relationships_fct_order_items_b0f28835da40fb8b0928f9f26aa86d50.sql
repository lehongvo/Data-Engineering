select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex3"."public_dbt_test__audit"."relationships_fct_order_items_b0f28835da40fb8b0928f9f26aa86d50"
    
      
    ) dbt_internal_test