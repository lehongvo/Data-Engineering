select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex3"."public_dbt_test__audit"."relationships_fct_order_items_6605ef9332585c82f278ac817835eb79"
    
      
    ) dbt_internal_test