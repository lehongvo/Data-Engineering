
      
        delete from "dbt_db_ex3"."public"."fct_monthly_sales" as DBT_INTERNAL_DEST
        where (year, month) in (
            select distinct year, month
            from "fct_monthly_sales__dbt_tmp135658777247" as DBT_INTERNAL_SOURCE
        );

    

    insert into "dbt_db_ex3"."public"."fct_monthly_sales" ("year", "month", "year_month", "orders_count", "unique_customers", "total_sales_amount", "total_shipping_cost", "average_order_value", "total_items_sold", "completed_orders", "cancelled_orders", "electronics_sales", "clothing_sales", "footwear_sales", "accessories_sales", "electronics_items_sold", "clothing_items_sold", "footwear_items_sold", "accessories_items_sold", "new_customers", "cancellation_rate", "sales_growth_pct", "updated_at")
    (
        select "year", "month", "year_month", "orders_count", "unique_customers", "total_sales_amount", "total_shipping_cost", "average_order_value", "total_items_sold", "completed_orders", "cancelled_orders", "electronics_sales", "clothing_sales", "footwear_sales", "accessories_sales", "electronics_items_sold", "clothing_items_sold", "footwear_items_sold", "accessories_items_sold", "new_customers", "cancellation_rate", "sales_growth_pct", "updated_at"
        from "fct_monthly_sales__dbt_tmp135658777247"
    )
  