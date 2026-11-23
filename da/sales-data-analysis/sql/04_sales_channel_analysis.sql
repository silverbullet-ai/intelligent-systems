-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 04: Sales Channel Analysis
-- ============================================

-- 1. Sales Performance by Channel

SELECT
    SalesChannel,

    COUNT(*) AS total_orders,

    SUM(OrderQuantity) AS total_quantity,

    ROUND(
        SUM(OrderQuantity * UnitPrice * (1 - DiscountApplied)),
        2
    ) AS net_sales,

    ROUND(
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ),
        2
    ) AS total_profit,

    ROUND(
        100.0 * SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) / SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ),
        2
    ) AS profit_margin_percentage,

    ROUND(
        100.0 * SUM(
            OrderQuantity * UnitPrice * DiscountApplied
        ) / SUM(OrderQuantity * UnitPrice),
        2
    ) AS weighted_discount_percentage

FROM regional_sales

GROUP BY SalesChannel

ORDER BY net_sales DESC;


-- 2. Channel Contribution to Overall Business

WITH channel_metrics AS (
    SELECT
        SalesChannel,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) AS total_profit

    FROM regional_sales
    GROUP BY SalesChannel
)

SELECT
    SalesChannel,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        100.0 * net_sales / SUM(net_sales) OVER (),
        2
    ) AS sales_contribution_percentage,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        100.0 * total_profit / SUM(total_profit) OVER (),
        2
    ) AS profit_contribution_percentage

FROM channel_metrics
ORDER BY net_sales DESC;


-- 3. Average Order Value and Profit per Order by Channel

SELECT
    SalesChannel,

    COUNT(*) AS total_orders,

    ROUND(
        SUM(OrderQuantity * UnitPrice * (1 - DiscountApplied))
        / COUNT(*),
        2
    ) AS average_order_value,

    ROUND(
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) / COUNT(*),
        2
    ) AS average_profit_per_order,

    ROUND(
        SUM(OrderQuantity) * 1.0 / COUNT(*),
        2
    ) AS average_quantity_per_order

FROM regional_sales

GROUP BY SalesChannel

ORDER BY average_order_value DESC;

