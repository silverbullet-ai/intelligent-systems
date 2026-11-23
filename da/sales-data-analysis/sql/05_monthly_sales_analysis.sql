-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 05: Monthly Sales Analysis
-- ============================================

-- 1. Convert dates into SQLite-compatible format

SELECT
    OrderDate AS original_date,

    SUBSTR(OrderDate, 7, 4) || '-' ||
    SUBSTR(OrderDate, 4, 2) || '-' ||
    SUBSTR(OrderDate, 1, 2) AS converted_date,

    STRFTIME(
        '%Y-%m',
        SUBSTR(OrderDate, 7, 4) || '-' ||
        SUBSTR(OrderDate, 4, 2) || '-' ||
        SUBSTR(OrderDate, 1, 2)
    ) AS order_month

FROM regional_sales
LIMIT 10;


-- 2. Monthly Sales Performance
-- Exclude partial May 2018

WITH monthly_sales AS (
    SELECT
        STRFTIME(
            '%Y-%m',
            SUBSTR(OrderDate, 7, 4) || '-' ||
            SUBSTR(OrderDate, 4, 2) || '-' ||
            SUBSTR(OrderDate, 1, 2)
        ) AS order_month,

        COUNT(*) AS total_orders,

        SUM(OrderQuantity) AS total_quantity,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) AS total_profit

    FROM regional_sales

    GROUP BY order_month
)

SELECT
    order_month,
    total_orders,
    total_quantity,
    ROUND(net_sales, 2) AS net_sales,
    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        100.0 * total_profit / net_sales,
        2
    ) AS profit_margin_percentage

FROM monthly_sales

WHERE order_month > '2018-05'

ORDER BY order_month;


-- 3. Month-over-Month Sales Growth
-- Exclude partial May 2018 before applying LAG()

WITH monthly_sales AS (
    SELECT
        SUBSTR(OrderDate, 7, 4) || '-' ||
        SUBSTR(OrderDate, 4, 2) AS order_month,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales

    FROM regional_sales

    GROUP BY order_month
),

complete_months AS (
    SELECT *
    FROM monthly_sales
    WHERE order_month > '2018-05'
),

monthly_growth AS (
    SELECT
        order_month,
        net_sales,

        LAG(net_sales) OVER (
            ORDER BY order_month
        ) AS previous_month_sales

    FROM complete_months
)

SELECT
    order_month,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(previous_month_sales, 2) AS previous_month_sales,

    ROUND(
        100.0 * (net_sales - previous_month_sales)
        / previous_month_sales,
        2
    ) AS mom_growth_percentage

FROM monthly_growth

ORDER BY order_month;


-- 4. Monthly Growth Summary

WITH monthly_sales AS (
    SELECT
        SUBSTR(OrderDate, 7, 4) || '-' ||
        SUBSTR(OrderDate, 4, 2) AS order_month,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales

    FROM regional_sales
    GROUP BY order_month
),

complete_months AS (
    SELECT *
    FROM monthly_sales
    WHERE order_month > '2018-05'
),

monthly_growth AS (
    SELECT
        order_month,
        net_sales,

        LAG(net_sales) OVER (
            ORDER BY order_month
        ) AS previous_month_sales

    FROM complete_months
),

growth_metrics AS (
    SELECT
        order_month,

        100.0 * (
            net_sales - previous_month_sales
        ) / previous_month_sales AS growth_percentage

    FROM monthly_growth
    WHERE previous_month_sales IS NOT NULL
)

SELECT
    COUNT(*) AS total_comparisons,

    SUM(CASE
        WHEN growth_percentage > 0 THEN 1
        ELSE 0
    END) AS positive_growth_months,

    SUM(CASE
        WHEN growth_percentage < 0 THEN 1
        ELSE 0
    END) AS negative_growth_months,

    ROUND(AVG(growth_percentage), 2)
        AS average_mom_growth,

    ROUND(MAX(growth_percentage), 2)
        AS highest_mom_growth,

    ROUND(MIN(growth_percentage), 2)
        AS lowest_mom_growth

FROM growth_metrics;

-- 5. Highest and Lowest Sales Months

WITH monthly_sales AS (
    SELECT
        SUBSTR(OrderDate, 7, 4) || '-' ||
        SUBSTR(OrderDate, 4, 2) AS order_month,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales

    FROM regional_sales
    GROUP BY order_month
),

complete_months AS (
    SELECT *
    FROM monthly_sales
    WHERE order_month > '2018-05'
)

SELECT
    'Highest Sales' AS performance,
    order_month,
    ROUND(net_sales, 2) AS net_sales
FROM complete_months
WHERE net_sales = (SELECT MAX(net_sales) FROM complete_months)

UNION ALL

SELECT
    'Lowest Sales' AS performance,
    order_month,
    ROUND(net_sales, 2) AS net_sales
FROM complete_months
WHERE net_sales = (SELECT MIN(net_sales) FROM complete_months);
