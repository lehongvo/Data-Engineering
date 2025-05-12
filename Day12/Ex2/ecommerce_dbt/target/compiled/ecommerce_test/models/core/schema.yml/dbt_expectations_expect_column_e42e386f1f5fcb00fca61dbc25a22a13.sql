with relation_columns as (

        
        select
            cast('CUSTOMER_ID' as TEXT) as relation_column,
            cast('INTEGER' as TEXT) as relation_column_type
        union all
        
        select
            cast('NAME' as TEXT) as relation_column,
            cast('CHARACTER VARYING' as TEXT) as relation_column_type
        union all
        
        select
            cast('EMAIL' as TEXT) as relation_column,
            cast('TEXT' as TEXT) as relation_column_type
        union all
        
        select
            cast('CREATED_AT' as TEXT) as relation_column,
            cast('TIMESTAMP WITHOUT TIME ZONE' as TEXT) as relation_column_type
        union all
        
        select
            cast('LIFETIME_ORDERS' as TEXT) as relation_column,
            cast('BIGINT' as TEXT) as relation_column_type
        union all
        
        select
            cast('FIRST_ORDER_DATE' as TEXT) as relation_column,
            cast('TIMESTAMP WITHOUT TIME ZONE' as TEXT) as relation_column_type
        union all
        
        select
            cast('MOST_RECENT_ORDER_DATE' as TEXT) as relation_column,
            cast('TIMESTAMP WITHOUT TIME ZONE' as TEXT) as relation_column_type
        union all
        
        select
            cast('UPDATED_AT' as TEXT) as relation_column,
            cast('TIMESTAMP WITH TIME ZONE' as TEXT) as relation_column_type
        
        
    ),
    test_data as (

        select
            *
        from
            relation_columns
        where
            relation_column = 'FIRST_ORDER_DATE'
            and
            relation_column_type not in ('TIMESTAMP')

    )
    select *
    from test_data