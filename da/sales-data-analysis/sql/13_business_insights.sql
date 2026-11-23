-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 13: Business Insights
-- ============================================


-- Query 1: Executive KPI Scorecard


WITH order_metrics AS (
    SELECT
        OrderNumber,
        OrderQuantity,
        DiscountApplied,

        OrderQuantity * UnitPrice AS gross_sales,

        (OrderQuantity * UnitPrice) * DiscountApplied
            AS discount_amount,

        (OrderQuantity * UnitPrice)
        - ((OrderQuantity * UnitPrice) * DiscountApplied)
            AS net_sales,

        OrderQuantity * UnitCost AS total_cost,

        (
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) - (OrderQuantity * UnitCost) AS profit,

        CAST(
            JULIANDAY(
                DATE(
                    SUBSTR(DeliveryDate, 7, 4) || '-' ||
                    SUBSTR(DeliveryDate, 4, 2) || '-' ||
                    SUBSTR(DeliveryDate, 1, 2)
                )
            )
            -
            JULIANDAY(
                DATE(
                    SUBSTR(OrderDate, 7, 4) || '-' ||
                    SUBSTR(OrderDate, 4, 2) || '-' ||
                    SUBSTR(OrderDate, 1, 2)
                )
            )
            AS INTEGER
        ) AS fulfillment_days

    FROM regional_sales
)

SELECT
    COUNT(*) AS total_orders,
    SUM(OrderQuantity) AS total_quantity,

    ROUND(SUM(gross_sales), 2) AS gross_sales,
    ROUND(SUM(discount_amount), 2) AS total_discount,
    ROUND(SUM(net_sales), 2) AS net_sales,
    ROUND(SUM(total_cost), 2) AS total_cost,
    ROUND(SUM(profit), 2) AS total_profit,

    ROUND(
        SUM(profit) * 100.0 / NULLIF(SUM(net_sales), 0), 2
    ) AS profit_margin,

    ROUND(
        SUM(discount_amount) * 100.0 /
        NULLIF(SUM(gross_sales), 0), 2
    ) AS weighted_discount_rate,

    ROUND(
        SUM(net_sales) / COUNT(*), 2
    ) AS average_order_value,

    SUM(
        CASE WHEN profit < 0 THEN 1 ELSE 0 END
    ) AS loss_making_orders,

    ROUND(
        SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS loss_order_percentage,

    ROUND(AVG(fulfillment_days), 2)
        AS average_fulfillment_days

FROM order_metrics;


-- Query 2: Sales Channel Performance


WITH channel_metrics AS (
    SELECT
        SalesChannel,
        COUNT(*) AS total_orders,
        SUM(OrderQuantity) AS total_quantity,

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) AS net_sales,

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        ) AS total_profit,

        SUM(
            (OrderQuantity * UnitPrice) * DiscountApplied
        ) AS discount_amount,

        SUM(OrderQuantity * UnitPrice) AS gross_sales,

        AVG(
            JULIANDAY(
                DATE(
                    SUBSTR(DeliveryDate, 7, 4) || '-' ||
                    SUBSTR(DeliveryDate, 4, 2) || '-' ||
                    SUBSTR(DeliveryDate, 1, 2)
                )
            )
            -
            JULIANDAY(
                DATE(
                    SUBSTR(OrderDate, 7, 4) || '-' ||
                    SUBSTR(OrderDate, 4, 2) || '-' ||
                    SUBSTR(OrderDate, 1, 2)
                )
            )
        ) AS average_fulfillment_days

    FROM regional_sales
    GROUP BY SalesChannel
)

SELECT
    SalesChannel,
    total_orders,
    total_quantity,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        net_sales * 100.0 /
        SUM(net_sales) OVER (), 2
    ) AS sales_contribution_percentage,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_profit * 100.0 /
        SUM(total_profit) OVER (), 2
    ) AS profit_contribution_percentage,

    ROUND(
        total_profit * 100.0 / NULLIF(net_sales, 0), 2
    ) AS profit_margin,

    ROUND(
        discount_amount * 100.0 /
        NULLIF(gross_sales, 0), 2
    ) AS weighted_discount_rate,

    ROUND(average_fulfillment_days, 2)
        AS average_fulfillment_days

FROM channel_metrics
ORDER BY net_sales DESC;


-- Query 3: Warehouse Performance


WITH warehouse_metrics AS (
    SELECT
        WarehouseCode,
        COUNT(*) AS total_orders,
        SUM(OrderQuantity) AS total_quantity,

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) AS net_sales,

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        ) AS total_profit,

        AVG(
            JULIANDAY(
                DATE(
                    SUBSTR(DeliveryDate, 7, 4) || '-' ||
                    SUBSTR(DeliveryDate, 4, 2) || '-' ||
                    SUBSTR(DeliveryDate, 1, 2)
                )
            )
            -
            JULIANDAY(
                DATE(
                    SUBSTR(OrderDate, 7, 4) || '-' ||
                    SUBSTR(OrderDate, 4, 2) || '-' ||
                    SUBSTR(OrderDate, 1, 2)
                )
            )
        ) AS average_fulfillment_days

    FROM regional_sales
    GROUP BY WarehouseCode
)

SELECT
    WarehouseCode,
    total_orders,
    total_quantity,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        net_sales * 100.0 /
        SUM(net_sales) OVER (), 2
    ) AS sales_contribution_percentage,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_profit * 100.0 /
        SUM(total_profit) OVER (), 2
    ) AS profit_contribution_percentage,

    ROUND(
        total_profit * 100.0 / NULLIF(net_sales, 0), 2
    ) AS profit_margin,

    ROUND(average_fulfillment_days, 2)
        AS average_fulfillment_days

FROM warehouse_metrics
ORDER BY net_sales DESC;


-- Query 4: Discount Risk Analysis


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
        ) - (OrderQuantity * UnitCost) AS profit

    FROM regional_sales
),

discount_groups AS (
    SELECT
        CASE
            WHEN DiscountApplied < 0.10 THEN 'Below 10%'
            WHEN DiscountApplied < 0.20 THEN '10% to 19.99%'
            WHEN DiscountApplied < 0.30 THEN '20% to 29.99%'
            ELSE '30% and Above'
        END AS discount_category,

        COUNT(*) AS total_orders,
        SUM(net_sales) AS net_sales,
        SUM(profit) AS total_profit,

        SUM(
            CASE WHEN profit < 0 THEN 1 ELSE 0 END
        ) AS loss_making_orders,

        SUM(
            CASE WHEN profit < 0 THEN profit ELSE 0 END
        ) AS total_loss_amount

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
        loss_making_orders * 100.0 /
        total_orders, 2
    ) AS loss_order_percentage,

    ROUND(total_loss_amount, 2) AS total_loss_amount,

    ROUND(
        ABS(total_loss_amount) * 100.0 /
        NULLIF(
            SUM(ABS(total_loss_amount)) OVER (), 0
        ), 2
    ) AS share_of_total_loss_amount

FROM discount_groups

ORDER BY
    CASE discount_category
        WHEN 'Below 10%' THEN 1
        WHEN '10% to 19.99%' THEN 2
        WHEN '20% to 29.99%' THEN 3
        ELSE 4
    END;


-- Query 5: Top Business Contributors


WITH entity_performance AS (

    -- Product Performance
    SELECT
        'Product' AS entity_type,
        CAST(ProductID AS TEXT) AS entity_id,

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) AS net_sales,

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        ) AS total_profit

    FROM regional_sales
    GROUP BY ProductID

    UNION ALL

    -- Customer Performance
    SELECT
        'Customer',
        CAST(CustomerID AS TEXT),

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ),

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        )

    FROM regional_sales
    GROUP BY CustomerID

    UNION ALL

    -- Sales Team Performance
    SELECT
        'Sales Team',
        CAST(SalesTeamID AS TEXT),

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ),

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        )

    FROM regional_sales
    GROUP BY SalesTeamID

    UNION ALL

    -- Store Performance
    SELECT
        'Store',
        CAST(StoreID AS TEXT),

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ),

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        )

    FROM regional_sales
    GROUP BY StoreID
),

ranked_entities AS (
    SELECT
        entity_type,
        entity_id,
        net_sales,
        total_profit,

        ROW_NUMBER() OVER (
            PARTITION BY entity_type
            ORDER BY net_sales DESC
        ) AS sales_rank,

        SUM(net_sales) OVER (
            PARTITION BY entity_type
        ) AS entity_type_sales

    FROM entity_performance
)

SELECT
    entity_type,
    sales_rank,
    entity_id,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        net_sales * 100.0 /
        NULLIF(entity_type_sales, 0), 2
    ) AS contribution_percentage,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_profit * 100.0 / NULLIF(net_sales, 0), 2
    ) AS profit_margin

FROM ranked_entities
WHERE sales_rank <= 5
ORDER BY
    CASE entity_type
        WHEN 'Product' THEN 1
        WHEN 'Customer' THEN 2
        WHEN 'Sales Team' THEN 3
        WHEN 'Store' THEN 4
    END,
    sales_rank;


-- Query 6: Monthly Business Performance Trends


WITH monthly_metrics AS (
    SELECT
        SUBSTR(OrderDate, 7, 4) || '-' ||
        SUBSTR(OrderDate, 4, 2) AS order_month,

        COUNT(*) AS total_orders,

        SUM(
            (OrderQuantity * UnitPrice)
            - ((OrderQuantity * UnitPrice) * DiscountApplied)
        ) AS net_sales,

        SUM(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        ) AS total_profit,

        AVG(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        ) AS average_order_profit,

        AVG(
            JULIANDAY(
                DATE(
                    SUBSTR(DeliveryDate, 7, 4) || '-' ||
                    SUBSTR(DeliveryDate, 4, 2) || '-' ||
                    SUBSTR(DeliveryDate, 1, 2)
                )
            )
            -
            JULIANDAY(
                DATE(
                    SUBSTR(OrderDate, 7, 4) || '-' ||
                    SUBSTR(OrderDate, 4, 2) || '-' ||
                    SUBSTR(OrderDate, 1, 2)
                )
            )
        ) AS average_fulfillment_days

    FROM regional_sales

    GROUP BY
        SUBSTR(OrderDate, 7, 4) || '-' ||
        SUBSTR(OrderDate, 4, 2)
),

complete_months AS (
    SELECT *
    FROM monthly_metrics
    WHERE order_month > '2018-05'
),

monthly_growth AS (
    SELECT
        *,

        LAG(net_sales) OVER (
            ORDER BY order_month
        ) AS previous_month_sales,

        LAG(total_profit) OVER (
            ORDER BY order_month
        ) AS previous_month_profit,

        LAG(average_fulfillment_days) OVER (
            ORDER BY order_month
        ) AS previous_month_fulfillment

    FROM complete_months
)

SELECT
    order_month,
    total_orders,

    ROUND(net_sales, 2) AS net_sales,

    ROUND(
        total_profit, 2
    ) AS total_profit,

    ROUND(
        total_profit * 100.0 /
        NULLIF(net_sales, 0), 2
    ) AS profit_margin,

    ROUND(
        average_order_profit, 2
    ) AS average_order_profit,

    ROUND(
        average_fulfillment_days, 2
    ) AS average_fulfillment_days,

    ROUND(
        (net_sales - previous_month_sales) * 100.0 /
        NULLIF(previous_month_sales, 0), 2
    ) AS sales_mom_change_percentage,

    ROUND(
        (total_profit - previous_month_profit) * 100.0 /
        NULLIF(previous_month_profit, 0), 2
    ) AS profit_mom_change_percentage,

    ROUND(
        average_fulfillment_days -
        previous_month_fulfillment, 2
    ) AS fulfillment_change_days

FROM monthly_growth
ORDER BY order_month;
