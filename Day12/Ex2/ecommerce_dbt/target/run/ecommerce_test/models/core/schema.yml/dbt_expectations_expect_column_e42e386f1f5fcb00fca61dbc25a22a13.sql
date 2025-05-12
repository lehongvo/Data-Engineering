select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
        select *
        from "dbt_db_ex2"."public_dbt_test__audit"."dbt_expectations_expect_column_e42e386f1f5fcb00fca61dbc25a22a13"
    
      
    ) dbt_internal_test