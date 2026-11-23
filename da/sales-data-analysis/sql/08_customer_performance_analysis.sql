-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 08: Customer Analysis
-- ============================================

-- 1. Customer Performance Overview

SELECT
    CustomerID,

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
        ) /
        SUM(OrderQuantity * UnitPrice * (1 - DiscountApplied)),
        2
    ) AS profit_margin_percentage

FROM regional_sales

GROUP BY CustomerID

ORDER BY net_sales DESC;

-- 2. Customer Contribution to Total Sales and Profit

WITH customer_metrics AS (
    SELECT
        CustomerID,

        SUM(
            OrderQuantity * UnitPrice
            - (OrderQuantity * UnitPrice * DiscountApplied)
        ) AS net_sales,

        SUM(
            OrderQuantity * UnitPrice
            - (OrderQuantity * UnitPrice * DiscountApplied)
            - (OrderQuantity * UnitCost)
        ) AS total_profit

    FROM regional_sales
    GROUP BY CustomerID
)

SELECT
    CustomerID,

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

FROM customer_metrics

ORDER BY net_sales DESC;

-- 3. Cumulative Customer Sales Contribution

WITH customer_sales AS (
    SELECT
        CustomerID,
        SUM(
            OrderQuantity * UnitPrice
            - (OrderQuantity * UnitPrice * DiscountApplied)
        ) AS net_sales
    FROM regional_sales
    GROUP BY CustomerID
),

ranked_customers AS (
    SELECT
        CustomerID,
        net_sales,

        ROW_NUMBER() OVER (
            ORDER BY net_sales DESC
        ) AS customer_rank,

        SUM(net_sales) OVER (
            ORDER BY net_sales DESC
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_sales

    FROM customer_sales
)

SELECT
    CustomerID,
    customer_rank,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        100.0 * net_sales / SUM(net_sales) OVER (),
        2
    ) AS sales_contribution_percentage,

    ROUND(
        100.0 * cumulative_sales / SUM(net_sales) OVER (),
        2
    ) AS cumulative_sales_contribution_percentage

FROM ranked_customers

ORDER BY customer_rank;

-- 4. Customer Profitability Ranking

SELECT
    CustomerID,

    COUNT(*) AS total_orders,

    ROUND(
        SUM(
            (OrderQuantity * UnitPrice)
            - (OrderQuantity * UnitPrice * DiscountApplied)
            - (OrderQuantity * UnitCost)
        ),
        2
    ) AS total_profit,

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

GROUP BY CustomerID

ORDER BY profit_margin_percentage DESC;

-- 5. Customer Discount Analysis

SELECT
    CustomerID,

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

GROUP BY CustomerID

ORDER BY weighted_discount_percentage DESC;

-- 6. Loss-Making Orders by Customer

WITH calculated_metrics AS (
    SELECT
        OrderNumber,
        CustomerID,

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
        CustomerID,
        net_sales - total_cost AS profit

    FROM calculated_metrics
),

customer_losses AS (
    SELECT
        CustomerID,

        COUNT(*) AS total_orders,

        SUM(
            CASE WHEN profit < 0 THEN 1 ELSE 0 END
        ) AS loss_making_orders,

        SUM(
            CASE WHEN profit < 0 THEN -profit ELSE 0 END
        ) AS total_loss_amount

    FROM order_profit

    GROUP BY CustomerID
)

SELECT
    CustomerID,
    total_orders,
    loss_making_orders,

    ROUND(
        100.0 * loss_making_orders / total_orders,
        2
    ) AS loss_order_percentage,

    ROUND(total_loss_amount, 2) AS total_loss_amount

FROM customer_losses

WHERE loss_making_orders > 0

ORDER BY total_loss_amount DESC;