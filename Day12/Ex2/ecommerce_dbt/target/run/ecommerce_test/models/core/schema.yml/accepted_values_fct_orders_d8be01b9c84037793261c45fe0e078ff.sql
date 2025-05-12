select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."accepted_values_fct_orders_d8be01b9c84037793261c45fe0e078ff"
    
      
    ) dbt_internal_test