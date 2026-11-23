-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 03: Overall Performance Analysis
-- ============================================

-- 1. Overall Business KPIs

WITH sales_metrics AS (
    SELECT
        COUNT(*) AS total_orders,
        SUM(OrderQuantity) AS total_quantity,

        SUM(OrderQuantity * UnitPrice) AS gross_sales,

        SUM(
            OrderQuantity * UnitPrice * DiscountApplied
        ) AS discount_amount,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales,

        SUM(OrderQuantity * UnitCost) AS total_cost,

        AVG(DiscountApplied) AS mean_order_discount,

        SUM(
            OrderQuantity * UnitPrice * DiscountApplied
        ) / SUM(OrderQuantity * UnitPrice) AS weighted_discount

    FROM regional_sales
)

SELECT
    total_orders,
    total_quantity,

    ROUND(gross_sales, 2) AS gross_sales,
    ROUND(discount_amount, 2) AS discount_amount,
    ROUND(net_sales, 2) AS net_sales,
    ROUND(total_cost, 2) AS total_cost,

    ROUND(net_sales - total_cost, 2) AS total_profit,

    ROUND(
        100.0 * (net_sales - total_cost) / net_sales,
        2
    ) AS profit_margin_percentage,

    ROUND(100.0 * mean_order_discount, 2)
        AS mean_order_discount_percentage,

    ROUND(100.0 * weighted_discount, 2)
        AS weighted_discount_percentage,

    ROUND(net_sales / total_orders, 2)
        AS average_order_value,

    ROUND((net_sales - total_cost) / total_orders, 2)
        AS average_profit_per_order

FROM sales_metrics;
