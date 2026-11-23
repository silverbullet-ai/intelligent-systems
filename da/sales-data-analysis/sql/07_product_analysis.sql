-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 07: Product Performance Analysis
-- ============================================

-- 1. Overall Product Performance

SELECT
    ProductID,

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
    ) AS profit_margin_percentage

FROM regional_sales

GROUP BY ProductID

ORDER BY net_sales DESC;


-- 2. Product Contribution to Overall Business

WITH product_metrics AS (
    SELECT
        ProductID,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) AS total_profit

    FROM regional_sales
    GROUP BY ProductID
)

SELECT
    ProductID,

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

FROM product_metrics

ORDER BY net_sales DESC;


-- 3. Cumulative Product Sales Contribution

WITH product_sales AS (
    SELECT
        ProductID,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales

    FROM regional_sales
    GROUP BY ProductID
),

ranked_products AS (
    SELECT
        ProductID,
        net_sales,

        ROW_NUMBER() OVER (
            ORDER BY net_sales DESC
        ) AS product_rank,

        SUM(net_sales) OVER (
            ORDER BY net_sales DESC, ProductID
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_sales

    FROM product_sales
),

concentration AS (
    SELECT
        product_rank,

        100.0 * cumulative_sales /
        SUM(net_sales) OVER () AS cumulative_sales_percentage

    FROM ranked_products
)

SELECT
    CASE
        WHEN cumulative_sales_percentage >= 50 THEN '50%'
        WHEN cumulative_sales_percentage >= 60 THEN '60%'
        WHEN cumulative_sales_percentage >= 70 THEN '70%'
        WHEN cumulative_sales_percentage >= 80 THEN '80%'
        WHEN cumulative_sales_percentage >= 90 THEN '90%'
    END AS sales_threshold,

    MIN(product_rank) AS products_required,

    ROUND(
        MIN(cumulative_sales_percentage),
        2
    ) AS actual_cumulative_percentage

FROM concentration

WHERE cumulative_sales_percentage >= 50

GROUP BY sales_threshold

ORDER BY products_required;

-- 3. Cumulative Product Sales Contribution

WITH product_sales AS (
    SELECT
        ProductID,
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales
    FROM regional_sales
    GROUP BY ProductID
),

ranked_products AS (
    SELECT
        ProductID,
        net_sales,

        ROW_NUMBER() OVER (
            ORDER BY net_sales DESC, ProductID
        ) AS product_rank,

        SUM(net_sales) OVER (
            ORDER BY net_sales DESC, ProductID
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_sales,

        SUM(net_sales) OVER () AS total_sales

    FROM product_sales
)

SELECT
    ProductID,
    product_rank,
    ROUND(net_sales, 2) AS net_sales,
    ROUND(100.0 * net_sales / total_sales, 2) AS sales_contribution,
    ROUND(100.0 * cumulative_sales / total_sales, 2)
        AS cumulative_sales_contribution

FROM ranked_products
ORDER BY product_rank;

-- 4. Product Profitability Ranking

SELECT
    ProductID,

    ROUND(
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ), 2
    ) AS net_sales,

    ROUND(
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ), 2
    ) AS total_profit,

    ROUND(
        100.0 * SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) /
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ), 2
    ) AS profit_margin_percentage

FROM regional_sales

GROUP BY ProductID

ORDER BY profit_margin_percentage DESC;

-- 5. Product Discount Analysis

SELECT
    ProductID,

    ROUND(AVG(DiscountApplied) * 100, 2)
        AS average_discount_percentage,

    ROUND(
        SUM(OrderQuantity * UnitPrice * (1 - DiscountApplied)), 2
    ) AS net_sales,

    ROUND(
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ), 2
    ) AS total_profit,

    ROUND(
        100.0 * SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) /
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ), 2
    ) AS profit_margin_percentage

FROM regional_sales

GROUP BY ProductID

ORDER BY average_discount_percentage DESC;

-- 6. Correlation Components:
-- Average Discount vs Profit Margin

WITH product_metrics AS (
    SELECT
        ProductID,

        AVG(DiscountApplied) AS average_discount,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) /
        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS profit_margin

    FROM regional_sales
    GROUP BY ProductID
)

SELECT
    COUNT(*) AS product_count,
    ROUND(AVG(average_discount), 4) AS mean_discount,
    ROUND(AVG(profit_margin), 4) AS mean_profit_margin,

    ROUND(SUM(
        (average_discount - (
            SELECT AVG(average_discount) FROM product_metrics
        )) *
        (profit_margin - (
            SELECT AVG(profit_margin) FROM product_metrics
        ))
    ), 6) AS covariance_component

FROM product_metrics;

-- 7. Loss-Making Orders by Product
-- Classify orders using two-decimal currency precision

WITH order_profit AS (
    SELECT
        ProductID,

        ROUND(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost,
            2
        ) AS profit

    FROM regional_sales
)

SELECT
    ProductID,

    COUNT(*) AS total_orders,

    SUM(
        CASE WHEN profit < 0 THEN 1 ELSE 0 END
    ) AS loss_making_orders,

    ROUND(
        100.0 * SUM(
            CASE WHEN profit < 0 THEN 1 ELSE 0 END
        ) / COUNT(*), 2
    ) AS loss_order_percentage,

    ROUND(
        SUM(
            CASE WHEN profit < 0 THEN profit ELSE 0 END
        ), 2
    ) AS total_loss

FROM order_profit

GROUP BY ProductID

ORDER BY loss_making_orders DESC;

-- 8. Overall Product Loss Summary
-- Currency-rounded profit classification

WITH order_profit AS (
    SELECT
        ProductID,

        ROUND(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost,
            2
        ) AS profit

    FROM regional_sales
)

SELECT
    COUNT(DISTINCT ProductID) AS total_products,
    COUNT(*) AS total_orders,

    SUM(
        CASE WHEN profit < 0 THEN 1 ELSE 0 END
    ) AS loss_making_orders,

    ROUND(
        100.0 * SUM(
            CASE WHEN profit < 0 THEN 1 ELSE 0 END
        ) / COUNT(*), 2
    ) AS loss_order_percentage,

    ROUND(
        SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END), 2
    ) AS total_loss,

    ROUND(
        SUM(CASE WHEN profit >= 0 THEN profit ELSE 0 END), 2
    ) AS profit_from_non_loss_orders

FROM order_profit;

