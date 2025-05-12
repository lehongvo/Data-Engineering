select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."source_accepted_values_ecommer_3e5b67e5c60a477732a6235b190fde6e"
    
      
    ) dbt_internal_test