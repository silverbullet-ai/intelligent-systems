-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 06: Warehouse Performance Analysis
-- ============================================

-- 1. Overall Warehouse Performance

SELECT
    WarehouseCode,

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

GROUP BY WarehouseCode

ORDER BY net_sales DESC;


-- 2. Warehouse Contribution to Overall Business

WITH warehouse_metrics AS (
    SELECT
        WarehouseCode,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) AS total_profit

    FROM regional_sales
    GROUP BY WarehouseCode
)

SELECT
    WarehouseCode,

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

FROM warehouse_metrics

ORDER BY net_sales DESC;


-- 3. Warehouse Profitability Ranking

WITH warehouse_metrics AS (
    SELECT
        WarehouseCode,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) AS total_profit

    FROM regional_sales
    GROUP BY WarehouseCode
)

SELECT
    WarehouseCode,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        100.0 * total_profit / net_sales,
        2
    ) AS profit_margin_percentage,

    RANK() OVER (
        ORDER BY total_profit * 1.0 / net_sales DESC
    ) AS margin_rank

FROM warehouse_metrics

ORDER BY margin_rank;


-- 4. Warehouse Sales Concentration

WITH warehouse_sales AS (
    SELECT
        WarehouseCode,

        SUM(
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
        ) AS net_sales

    FROM regional_sales
    GROUP BY WarehouseCode
),

ranked_warehouses AS (
    SELECT
        WarehouseCode,
        net_sales,

        RANK() OVER (
            ORDER BY net_sales DESC
        ) AS sales_rank

    FROM warehouse_sales
)

SELECT
    COUNT(*) AS total_warehouses,

    ROUND(SUM(net_sales), 2) AS total_net_sales,

    ROUND(
        SUM(
            CASE WHEN sales_rank <= 3
            THEN net_sales ELSE 0 END
        ),
        2
    ) AS top_3_warehouse_sales,

    ROUND(
        100.0 * SUM(
            CASE WHEN sales_rank <= 3
            THEN net_sales ELSE 0 END
        ) / SUM(net_sales),
        2
    ) AS top_3_sales_contribution_percentage

FROM ranked_warehouses;

