-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 10: Store Performance Analysis
-- ============================================

-- 1. Store Performance Overview

WITH calculated_metrics AS (
    SELECT
        StoreID,
        OrderNumber,
        OrderQuantity,

        OrderQuantity * UnitPrice AS gross_sales,

        (OrderQuantity * UnitPrice) * DiscountApplied
            AS discount_amount,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        OrderQuantity * UnitCost AS total_cost

    FROM regional_sales
),

store_metrics AS (
    SELECT
        StoreID,

        COUNT(*) AS total_orders,

        SUM(OrderQuantity) AS total_quantity,

        SUM(net_sales) AS net_sales,

        SUM(net_sales - total_cost) AS total_profit

    FROM calculated_metrics

    GROUP BY StoreID
)

SELECT
    StoreID,
    total_orders,
    total_quantity,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        100.0 * total_profit / net_sales,
        2
    ) AS profit_margin_percentage

FROM store_metrics

ORDER BY net_sales DESC;

-- 2. Store Contribution to Total Sales and Profit

WITH store_metrics AS (
    SELECT
        StoreID,

        SUM(
            OrderQuantity * UnitPrice
            - (OrderQuantity * UnitPrice * DiscountApplied)
        ) AS net_sales,

        SUM(
            (OrderQuantity * UnitPrice)
            - (OrderQuantity * UnitPrice * DiscountApplied)
            - (OrderQuantity * UnitCost)
        ) AS total_profit

    FROM regional_sales

    GROUP BY StoreID
)

SELECT
    StoreID,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        100.0 * net_sales / SUM(net_sales) OVER (),
        2
    ) AS sales_contribution_percentage,

    ROUND(
        100.0 * total_profit / SUM(total_profit) OVER (),
        2
    ) AS profit_contribution_percentage

FROM store_metrics

ORDER BY net_sales DESC;

-- 3. Cumulative Store Sales Contribution

WITH store_sales AS (
    SELECT
        StoreID,

        SUM(
            OrderQuantity * UnitPrice
            - (OrderQuantity * UnitPrice * DiscountApplied)
        ) AS net_sales

    FROM regional_sales

    GROUP BY StoreID
),

ranked_stores AS (
    SELECT
        StoreID,
        net_sales,

        ROW_NUMBER() OVER (
            ORDER BY net_sales DESC
        ) AS store_rank,

        SUM(net_sales) OVER (
            ORDER BY net_sales DESC
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_sales

    FROM store_sales
)

SELECT
    StoreID,
    store_rank,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        100.0 * net_sales / SUM(net_sales) OVER (),
        2
    ) AS sales_contribution_percentage,

    ROUND(
        100.0 * cumulative_sales / SUM(net_sales) OVER (),
        2
    ) AS cumulative_sales_contribution_percentage

FROM ranked_stores

ORDER BY store_rank;

-- 4. Store Profitability Ranking

WITH calculated_metrics AS (
    SELECT
        StoreID,

        OrderQuantity * UnitPrice AS gross_sales,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        OrderQuantity * UnitCost AS total_cost

    FROM regional_sales
)

SELECT
    StoreID,

    COUNT(*) AS total_orders,

    ROUND(
        SUM(net_sales - total_cost),
        2
    ) AS total_profit,

    ROUND(
        100.0 * SUM(net_sales - total_cost)
        / SUM(net_sales),
        2
    ) AS profit_margin_percentage

FROM calculated_metrics

GROUP BY StoreID

ORDER BY profit_margin_percentage DESC;

-- 5. Store Discount Analysis

SELECT
    StoreID,

    COUNT(*) AS total_orders,

    ROUND(
        100.0 * AVG(DiscountApplied),
        2
    ) AS average_discount_percentage,

    ROUND(
        100.0 * SUM(
            OrderQuantity * UnitPrice * DiscountApplied
        ) /
        SUM(
            OrderQuantity * UnitPrice
        ),
        2
    ) AS weighted_discount_percentage,

    ROUND(
        100.0 * SUM(
            (OrderQuantity * UnitPrice)
            - (OrderQuantity * UnitPrice * DiscountApplied)
            - (OrderQuantity * UnitCost)
        ) /
        SUM(
            (OrderQuantity * UnitPrice)
            - (OrderQuantity * UnitPrice * DiscountApplied)
        ),
        2
    ) AS profit_margin_percentage

FROM regional_sales

GROUP BY StoreID

ORDER BY weighted_discount_percentage DESC;

-- 6. Loss-Making Orders by Store

WITH calculated_metrics AS (
    SELECT
        OrderNumber,
        StoreID,

        OrderQuantity * UnitPrice AS gross_sales,

        (OrderQuantity * UnitPrice) * DiscountApplied
            AS discount_amount,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        OrderQuantity * UnitCost AS total_cost

    FROM regional_sales
),

order_profit AS (
    SELECT
        OrderNumber,
        StoreID,

        net_sales - total_cost AS profit

    FROM calculated_metrics
),

store_losses AS (
    SELECT
        StoreID,

        COUNT(*) AS total_orders,

        SUM(
            CASE WHEN profit < 0 THEN 1 ELSE 0 END
        ) AS loss_making_orders,

        SUM(
            CASE WHEN profit < 0 THEN -profit ELSE 0 END
        ) AS total_loss_amount

    FROM order_profit

    GROUP BY StoreID
)

SELECT
    StoreID,
    total_orders,
    loss_making_orders,

    ROUND(
        100.0 * loss_making_orders / total_orders,
        2
    ) AS loss_order_percentage,

    ROUND(total_loss_amount, 2) AS total_loss_amount

FROM store_losses

WHERE loss_making_orders > 0

ORDER BY total_loss_amount DESC;