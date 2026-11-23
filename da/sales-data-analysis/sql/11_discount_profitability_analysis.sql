-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 11: Discount and Profitability Analysis
-- ============================================

-- Query 1: Discount Distribution

WITH discount_metrics AS (
    SELECT
        DiscountApplied,
        COUNT(*) AS total_orders,
        SUM(OrderQuantity) AS total_quantity,

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) AS net_sales,

        SUM(
            ((OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied))
            - (OrderQuantity * UnitCost)
        ) AS total_profit

    FROM regional_sales
    GROUP BY DiscountApplied
)

SELECT
    DiscountApplied,
    total_orders,
    ROUND(
        total_orders * 100.0 /
        SUM(total_orders) OVER (), 2
    ) AS order_percentage,
    total_quantity,
    ROUND(net_sales, 2) AS net_sales,
    ROUND(total_profit, 2) AS total_profit

FROM discount_metrics
ORDER BY DiscountApplied;


-- Query 2: Discount Rate vs Profitability

WITH order_metrics AS (
    SELECT
        DiscountApplied,

        OrderQuantity * UnitPrice AS gross_sales,

        (OrderQuantity * UnitPrice) * DiscountApplied
            AS discount_amount,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        OrderQuantity * UnitCost AS total_cost

    FROM regional_sales
),

discount_metrics AS (
    SELECT
        DiscountApplied,
        COUNT(*) AS total_orders,
        SUM(gross_sales) AS gross_sales,
        SUM(discount_amount) AS discount_amount,
        SUM(net_sales) AS net_sales,
        SUM(total_cost) AS total_cost,
        SUM(net_sales - total_cost) AS total_profit

    FROM order_metrics
    GROUP BY DiscountApplied
)

SELECT
    DiscountApplied,
    total_orders,
    ROUND(gross_sales, 2) AS gross_sales,
    ROUND(discount_amount, 2) AS discount_amount,
    ROUND(net_sales, 2) AS net_sales,
    ROUND(total_cost, 2) AS total_cost,
    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_profit * 100.0 / NULLIF(net_sales, 0),
        2
    ) AS profit_margin,

    ROUND(
        discount_amount * 100.0 / NULLIF(gross_sales, 0),
        2
    ) AS weighted_discount_rate

FROM discount_metrics
ORDER BY DiscountApplied;

-- Query 3: Loss-Making Orders by Discount Rate

WITH calculated_metrics AS (
    SELECT
        OrderNumber,
        DiscountApplied,

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
        DiscountApplied,
        net_sales - total_cost AS profit

    FROM calculated_metrics
)

SELECT
    DiscountApplied,

    COUNT(*) AS total_orders,

    SUM(
        CASE WHEN profit < 0 THEN 1 ELSE 0 END
    ) AS loss_making_orders,

    ROUND(
        SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS loss_order_percentage,

    ROUND(
        SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END), 2
    ) AS total_loss_amount,

    ROUND(
        AVG(CASE WHEN profit < 0 THEN -profit END), 2
    ) AS average_loss_per_loss_order

FROM order_profit
GROUP BY DiscountApplied
ORDER BY DiscountApplied;

-- Query 4: Discount Contribution to Sales and Profit

WITH discount_metrics AS (
    SELECT
        DiscountApplied,

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) AS net_sales,

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            )
            - (OrderQuantity * UnitCost)
        ) AS total_profit,

        SUM(
            (OrderQuantity * UnitPrice) * DiscountApplied
        ) AS discount_amount

    FROM regional_sales
    GROUP BY DiscountApplied
)

SELECT
    DiscountApplied,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        net_sales * 100.0 /
        SUM(net_sales) OVER (), 2
    ) AS sales_contribution_percentage,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_profit * 100.0 /
        NULLIF(SUM(total_profit) OVER (), 0), 2
    ) AS profit_contribution_percentage,

    ROUND(discount_amount, 2) AS discount_amount

FROM discount_metrics
ORDER BY net_sales DESC;

-- Query 5: High-Discount Order Analysis

WITH order_metrics AS (
    SELECT
        OrderNumber,
        DiscountApplied,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        (
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) - (OrderQuantity * UnitCost)
            AS profit

    FROM regional_sales
),

discount_groups AS (
    SELECT
        CASE
            WHEN DiscountApplied < 0.20 THEN 'Below 20%'
            WHEN DiscountApplied < 0.30 THEN '20% to 29.99%'
            ELSE '30% and Above'
        END AS discount_category,

        COUNT(*) AS total_orders,
        SUM(net_sales) AS net_sales,
        SUM(profit) AS total_profit,

        SUM(
            CASE WHEN profit < 0 THEN 1 ELSE 0 END
        ) AS loss_making_orders

    FROM order_metrics
    GROUP BY discount_category
)

SELECT
    discount_category,
    total_orders,

    ROUND(
        total_orders * 100.0 /
        SUM(total_orders) OVER (), 2
    ) AS order_percentage,

    ROUND(net_sales, 2) AS net_sales,
    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_profit * 100.0 / NULLIF(net_sales, 0), 2
    ) AS profit_margin,

    loss_making_orders,

    ROUND(
        loss_making_orders * 100.0 / total_orders, 2
    ) AS loss_order_percentage

FROM discount_groups
ORDER BY
    CASE discount_category
        WHEN 'Below 20%' THEN 1
        WHEN '20% to 29.99%' THEN 2
        ELSE 3
    END;


-- Query 6: Discount vs Profit Margin Correlation

WITH order_metrics AS (
    SELECT
        OrderNumber,
        DiscountApplied,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        (
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) - (OrderQuantity * UnitCost)
            AS profit

    FROM regional_sales
)

SELECT
    OrderNumber,
    DiscountApplied,
    net_sales,
    profit,

    profit * 1.0 / NULLIF(net_sales, 0)
        AS profit_margin

FROM order_metrics
ORDER BY OrderNumber;
