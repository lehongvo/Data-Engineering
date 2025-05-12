# dbt Test Report

## Summary

- Total tests run: 26
- Tests passed: 25
- Tests failed: 1

## Details

- 16:[0m06:24:27  1 of 25 PASS accepted_values_dim_products_category__Electronics__Clothing__Footwear__Accessories  [[32mPASS[0m in 0.12s]
- 17:[0m06:24:27  2 of 25 PASS accepted_values_fct_orders_status__completed__processing__cancelled__refunded  [[32mPASS[0m in 0.12s]
- 20:[0m06:24:27  4 of 25 PASS assert_total_amount_equals_sum_of_items ........................... [[32mPASS[0m in 0.16s]
- 21:[0m06:24:27  3 of 25 FAIL 2 assert_no_duplicate_orders ...................................... [[31mFAIL 2[0m in 0.16s]
- 24:[0m06:24:27  5 of 25 PASS dbt_expectations_expect_column_values_to_match_regex_dim_customers_email___a_z0_9___a_z0_9_a_z_2_  [[32mPASS[0m in 0.11s]
- 26:[0m06:24:27  6 of 25 PASS not_null_dim_customers_customer_id ................................ [[32mPASS[0m in 0.13s]
- 28:[0m06:24:27  7 of 25 PASS not_null_dim_customers_email ...................................... [[32mPASS[0m in 0.12s]
- 29:[0m06:24:27  8 of 25 PASS not_null_dim_customers_lifetime_orders ............................ [[32mPASS[0m in 0.12s]
- 32:[0m06:24:27  9 of 25 PASS not_null_dim_customers_name ....................................... [[32mPASS[0m in 0.07s]
- 34:[0m06:24:27  10 of 25 PASS not_null_dim_products_name ....................................... [[32mPASS[0m in 0.08s]
- 36:[0m06:24:28  11 of 25 PASS not_null_dim_products_price ...................................... [[32mPASS[0m in 0.08s]
- 38:[0m06:24:28  12 of 25 PASS not_null_dim_products_product_id ................................. [[32mPASS[0m in 0.08s]
- 40:[0m06:24:28  13 of 25 PASS not_null_dim_products_total_quantity_sold ........................ [[32mPASS[0m in 0.08s]
- 42:[0m06:24:28  14 of 25 PASS not_null_dim_products_total_revenue .............................. [[32mPASS[0m in 0.08s]
- 44:[0m06:24:28  15 of 25 PASS not_null_fct_orders_customer_id .................................. [[32mPASS[0m in 0.06s]
- 46:[0m06:24:28  16 of 25 PASS not_null_fct_orders_order_date ................................... [[32mPASS[0m in 0.08s]
- 48:[0m06:24:28  17 of 25 PASS not_null_fct_orders_order_id ..................................... [[32mPASS[0m in 0.08s]
- 50:[0m06:24:28  18 of 25 PASS not_null_fct_orders_status ....................................... [[32mPASS[0m in 0.12s]
- 52:[0m06:24:28  19 of 25 PASS not_null_fct_orders_total_amount ................................. [[32mPASS[0m in 0.14s]
- 54:[0m06:24:28  20 of 25 PASS not_null_fct_orders_total_items .................................. [[32mPASS[0m in 0.15s]
- 56:[0m06:24:28  21 of 25 PASS relationships_fct_orders_customer_id__customer_id__ref_dim_customers_  [[32mPASS[0m in 0.20s]
- 58:[0m06:24:28  22 of 25 PASS unique_dim_customers_customer_id ................................. [[32mPASS[0m in 0.17s]
- 59:[0m06:24:28  23 of 25 PASS unique_dim_customers_email ....................................... [[32mPASS[0m in 0.13s]
- 60:[0m06:24:28  24 of 25 PASS unique_dim_products_product_id ................................... [[32mPASS[0m in 0.05s]
- 61:[0m06:24:28  25 of 25 PASS unique_fct_orders_order_id ....................................... [[32mPASS[0m in 0.04s]
- 77:[0m06:24:28  Done. PASS=24 WARN=0 ERROR=1 SKIP=0 TOTAL=25

## Detailed Errors

```
[0m06:24:27  6 of 25 START test not_null_dim_customers_customer_id .......................... [RUN]
[0m06:24:27  4 of 25 PASS assert_total_amount_equals_sum_of_items ........................... [[32mPASS[0m in 0.16s]
[0m06:24:27  3 of 25 FAIL 2 assert_no_duplicate_orders ...................................... [[31mFAIL 2[0m in 0.16s]
[0m06:24:27  7 of 25 START test not_null_dim_customers_email ................................ [RUN]
[0m06:24:27  8 of 25 START test not_null_dim_customers_lifetime_orders ...................... [RUN]
[0m06:24:27  5 of 25 PASS dbt_expectations_expect_column_values_to_match_regex_dim_customers_email___a_z0_9___a_z0_9_a_z_2_  [[32mPASS[0m in 0.11s]
[0m06:24:27  9 of 25 START test not_null_dim_customers_name ................................. [RUN]
[0m06:24:27  6 of 25 PASS not_null_dim_customers_customer_id ................................ [[32mPASS[0m in 0.13s]
[0m06:24:27  10 of 25 START test not_null_dim_products_name ................................. [RUN]
[0m06:24:27  7 of 25 PASS not_null_dim_customers_email ...................................... [[32mPASS[0m in 0.12s]
[0m06:24:27  8 of 25 PASS not_null_dim_customers_lifetime_orders ............................ [[32mPASS[0m in 0.12s]
[0m06:24:27  11 of 25 START test not_null_dim_products_price ................................ [RUN]
[0m06:24:27  12 of 25 START test not_null_dim_products_product_id ........................... [RUN]
```
