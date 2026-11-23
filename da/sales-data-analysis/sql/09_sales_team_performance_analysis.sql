-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 09: Sales Team Performance Analysis
-- ============================================

-- 1. Sales Team Performance Overview

WITH calculated_metrics AS (
    SELECT
        SalesTeamID,
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

team_metrics AS (
    SELECT
        SalesTeamID,

        COUNT(*) AS total_orders,

        SUM(OrderQuantity) AS total_quantity,

        SUM(net_sales) AS net_sales,

        SUM(net_sales - total_cost) AS total_profit

    FROM calculated_metrics

    GROUP BY SalesTeamID
)

SELECT
    SalesTeamID,
    total_orders,
    total_quantity,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        100.0 * total_profit / net_sales,
        2
    ) AS profit_margin_percentage

FROM team_metrics

ORDER BY net_sales DESC;

-- 2. Sales Team Contribution to Total Sales and Profit

WITH team_metrics AS (
    SELECT
        SalesTeamID,

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
    GROUP BY SalesTeamID
)

SELECT
    SalesTeamID,

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

FROM team_metrics
ORDER BY net_sales DESC;

-- 3. Cumulative Sales Team Contribution

WITH team_sales AS (
    SELECT
        SalesTeamID,

        SUM(
            OrderQuantity * UnitPrice
            - (OrderQuantity * UnitPrice * DiscountApplied)
        ) AS net_sales

    FROM regional_sales
    GROUP BY SalesTeamID
),

ranked_teams AS (
    SELECT
        SalesTeamID,
        net_sales,

        ROW_NUMBER() OVER (
            ORDER BY net_sales DESC
        ) AS team_rank,

        SUM(net_sales) OVER (
            ORDER BY net_sales DESC
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_sales

    FROM team_sales
)

SELECT
    SalesTeamID,
    team_rank,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        100.0 * net_sales / SUM(net_sales) OVER (),
        2
    ) AS sales_contribution_percentage,

    ROUND(
        100.0 * cumulative_sales / SUM(net_sales) OVER (),
        2
    ) AS cumulative_sales_contribution_percentage

FROM ranked_teams
ORDER BY team_rank;

-- 4. Sales Team Profitability Ranking

WITH calculated_metrics AS (
    SELECT
        SalesTeamID,
        OrderQuantity * UnitPrice AS gross_sales,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        OrderQuantity * UnitCost AS total_cost

    FROM regional_sales
)

SELECT
    SalesTeamID,

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

GROUP BY SalesTeamID

ORDER BY profit_margin_percentage DESC;

-- 5. Sales Team Discount Analysis

SELECT
    SalesTeamID,

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

GROUP BY SalesTeamID

ORDER BY weighted_discount_percentage DESC;

-- 6. Loss-Making Orders by Sales Team

WITH calculated_metrics AS (
    SELECT
        OrderNumber,
        SalesTeamID,

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
        SalesTeamID,
        net_sales - total_cost AS profit

    FROM calculated_metrics
),

team_losses AS (
    SELECT
        SalesTeamID,

        COUNT(*) AS total_orders,

        SUM(
            CASE WHEN profit < 0 THEN 1 ELSE 0 END
        ) AS loss_making_orders,

        SUM(
            CASE WHEN profit < 0 THEN -profit ELSE 0 END
        ) AS total_loss_amount

    FROM order_profit

    GROUP BY SalesTeamID
)

SELECT
    SalesTeamID,
    total_orders,
    loss_making_orders,

    ROUND(
        100.0 * loss_making_orders / total_orders,
        2
    ) AS loss_order_percentage,

    ROUND(total_loss_amount, 2) AS total_loss_amount

FROM team_losses

WHERE loss_making_orders > 0

ORDER BY total_loss_amount DESC;