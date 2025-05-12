
      
        
        
        delete from "dbt_db_ex3"."public"."stg_order_items" as DBT_INTERNAL_DEST
        where (order_item_id) in (
            select distinct order_item_id
            from "stg_order_items__dbt_tmp135648095464" as DBT_INTERNAL_SOURCE
        );

    

    insert into "dbt_db_ex3"."public"."stg_order_items" ("order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_amount", "item_total", "created_at", "updated_at")
    (
        select "order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_amount", "item_total", "created_at", "updated_at"
        from "stg_order_items__dbt_tmp135648095464"
    )
  