
      
        
        
        delete from "dbt_db_ex3"."public"."stg_orders" as DBT_INTERNAL_DEST
        where (order_id) in (
            select distinct order_id
            from "stg_orders__dbt_tmp135648186208" as DBT_INTERNAL_SOURCE
        );

    

    insert into "dbt_db_ex3"."public"."stg_orders" ("order_id", "customer_id", "order_date", "status", "payment_method", "shipping_address", "shipping_cost", "total_amount", "created_at", "updated_at")
    (
        select "order_id", "customer_id", "order_date", "status", "payment_method", "shipping_address", "shipping_cost", "total_amount", "created_at", "updated_at"
        from "stg_orders__dbt_tmp135648186208"
    )
  