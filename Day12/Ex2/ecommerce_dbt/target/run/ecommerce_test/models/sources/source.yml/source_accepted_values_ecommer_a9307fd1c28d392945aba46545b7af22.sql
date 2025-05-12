select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."source_accepted_values_ecommer_a9307fd1c28d392945aba46545b7af22"
    
      
    ) dbt_internal_test