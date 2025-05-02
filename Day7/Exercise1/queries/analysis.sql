-- 1. Total revenue by segment
SELECT
    Segment,
    SUM(`Weighted Revenue`) as total_revenue,
    COUNT(*) as opportunity_count
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
GROUP BY
    Segment
ORDER BY
    total_revenue DESC;

-- 2. Sales trend by date
SELECT
    Date,
    SUM(`Weighted Revenue`) as daily_revenue,
    COUNT(*) as opportunity_count
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
GROUP BY
    Date
ORDER BY
    Date;

-- 3. Top salespeople by revenue
SELECT
    Salesperson,
    SUM(`Weighted Revenue`) as total_revenue,
    COUNT(*) as opportunity_count,
    AVG(`Weighted Revenue`) as avg_opportunity_value
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
GROUP BY
    Salesperson
ORDER BY
    total_revenue DESC
LIMIT
    5;

-- 4. Opportunity stage analysis
SELECT
    `Opportunity Stage`,
    SUM(`Weighted Revenue`) as total_revenue,
    COUNT(*) as opportunity_count,
    AVG(`Weighted Revenue`) as avg_opportunity_value
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
GROUP BY
    `Opportunity Stage`
ORDER BY
    total_revenue DESC;

-- 5. Regional performance
SELECT
    Region,
    COUNT(DISTINCT Salesperson) as salespeople_count,
    SUM(`Weighted Revenue`) as total_revenue,
    COUNT(*) as opportunity_count,
    AVG(`Weighted Revenue`) as avg_opportunity_value
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
GROUP BY
    Region
ORDER BY
    total_revenue DESC;

-- 6. Active vs. Closed opportunities
SELECT
    `Active Opportunity`,
    `Closed Opportunity`,
    COUNT(*) as opportunity_count,
    SUM(`Weighted Revenue`) as total_revenue,
    AVG(`Weighted Revenue`) as avg_revenue
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
GROUP BY
    `Active Opportunity`,
    `Closed Opportunity`
ORDER BY
    opportunity_count DESC;

-- 7. Segment performance by region
SELECT
    Segment,
    Region,
    SUM(`Weighted Revenue`) as total_revenue,
    COUNT(*) as opportunity_count
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
GROUP BY
    Segment,
    Region
ORDER BY
    Segment,
    total_revenue DESC;

-- 8. Monthly forecasted revenue analysis
SELECT
    EXTRACT(
        MONTH
        FROM
            Date
    ) as month,
    EXTRACT(
        YEAR
        FROM
            Date
    ) as year,
    AVG(`Forecasted Monthly Revenue`) as avg_forecasted_revenue,
    SUM(`Forecasted Monthly Revenue`) as total_forecasted_revenue,
    COUNT(*) as opportunity_count
FROM
    `unique-axle-457602-n6.exercise1.sales-data_data`
WHERE
    `Forecasted Monthly Revenue` > 0
GROUP BY
    year,
    month
ORDER BY
    year,
    month;