-- ============================================
-- US REGIONAL SALES ANALYSIS
-- Module 12: Fulfillment Analysis
-- ============================================


-- Query 1: Overall Fulfillment Performance


WITH converted_dates AS (
    SELECT
        OrderNumber,

        DATE(
            SUBSTR(ProcuredDate, 7, 4) || '-' ||
            SUBSTR(ProcuredDate, 4, 2) || '-' ||
            SUBSTR(ProcuredDate, 1, 2)
        ) AS procured_date,

        DATE(
            SUBSTR(OrderDate, 7, 4) || '-' ||
            SUBSTR(OrderDate, 4, 2) || '-' ||
            SUBSTR(OrderDate, 1, 2)
        ) AS order_date,

        DATE(
            SUBSTR(ShipDate, 7, 4) || '-' ||
            SUBSTR(ShipDate, 4, 2) || '-' ||
            SUBSTR(ShipDate, 1, 2)
        ) AS ship_date,

        DATE(
            SUBSTR(DeliveryDate, 7, 4) || '-' ||
            SUBSTR(DeliveryDate, 4, 2) || '-' ||
            SUBSTR(DeliveryDate, 1, 2)
        ) AS delivery_date

    FROM regional_sales
),

fulfillment_metrics AS (
    SELECT
        'Procurement Lead Time' AS metric,
        CAST(
            JULIANDAY(ship_date) - JULIANDAY(procured_date)
            AS INTEGER
        ) AS duration_days
    FROM converted_dates

    UNION ALL

    SELECT
        'Order Processing Time',
        CAST(
            JULIANDAY(ship_date) - JULIANDAY(order_date)
            AS INTEGER
        )
    FROM converted_dates

    UNION ALL

    SELECT
        'Shipping Duration',
        CAST(
            JULIANDAY(delivery_date) - JULIANDAY(ship_date)
            AS INTEGER
        )
    FROM converted_dates

    UNION ALL

    SELECT
        'Total Fulfillment Time',
        CAST(
            JULIANDAY(delivery_date) - JULIANDAY(order_date)
            AS INTEGER
        )
    FROM converted_dates
),

ranked_metrics AS (
    SELECT
        metric,
        duration_days,

        ROW_NUMBER() OVER (
            PARTITION BY metric
            ORDER BY duration_days
        ) AS row_num,

        COUNT(*) OVER (
            PARTITION BY metric
        ) AS total_orders

    FROM fulfillment_metrics
    WHERE duration_days IS NOT NULL
)

SELECT
    metric,
    total_orders,

    ROUND(AVG(duration_days), 2) AS average_days,

    ROUND(
        AVG(
            CASE
                WHEN row_num IN (
                    (total_orders + 1) / 2,
                    (total_orders + 2) / 2
                )
                THEN duration_days
            END
        ), 2
    ) AS median_days,

    MAX(
        CASE
            WHEN row_num = (total_orders * 9 + 9) / 10
            THEN duration_days
        END
    ) AS p90_days,

    MIN(duration_days) AS minimum_days,
    MAX(duration_days) AS maximum_days

FROM ranked_metrics
GROUP BY metric, total_orders
ORDER BY
    CASE metric
        WHEN 'Procurement Lead Time' THEN 1
        WHEN 'Order Processing Time' THEN 2
        WHEN 'Shipping Duration' THEN 3
        WHEN 'Total Fulfillment Time' THEN 4
    END;


-- Query 2: Fulfillment Stage Analysi


WITH converted_dates AS (
    SELECT
        CAST(
            JULIANDAY(
                DATE(
                    SUBSTR(ShipDate, 7, 4) || '-' ||
                    SUBSTR(ShipDate, 4, 2) || '-' ||
                    SUBSTR(ShipDate, 1, 2)
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
        ) AS processing_days,

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
                    SUBSTR(ShipDate, 7, 4) || '-' ||
                    SUBSTR(ShipDate, 4, 2) || '-' ||
                    SUBSTR(ShipDate, 1, 2)
                )
            )
            AS INTEGER
        ) AS shipping_days

    FROM regional_sales
),

stage_metrics AS (
    SELECT
        'Order Processing' AS stage,
        processing_days AS duration_days
    FROM converted_dates

    UNION ALL

    SELECT
        'Shipping',
        shipping_days
    FROM converted_dates
)

SELECT
    stage,
    COUNT(*) AS total_orders,

    ROUND(AVG(duration_days), 2) AS average_days,
    MIN(duration_days) AS minimum_days,
    MAX(duration_days) AS maximum_days,

    ROUND(
        AVG(duration_days) * 100.0 /
        SUM(AVG(duration_days)) OVER (), 2
    ) AS fulfillment_time_percentage

FROM stage_metrics
WHERE duration_days IS NOT NULL
GROUP BY stage
ORDER BY
    CASE stage
        WHEN 'Order Processing' THEN 1
        WHEN 'Shipping' THEN 2
    END;


-- Query 3: Sales Channel Fulfillment Analysis


WITH fulfillment_metrics AS (
    SELECT
        SalesChannel,

        CAST(
            JULIANDAY(
                DATE(
                    SUBSTR(ShipDate, 7, 4) || '-' ||
                    SUBSTR(ShipDate, 4, 2) || '-' ||
                    SUBSTR(ShipDate, 1, 2)
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
        ) AS processing_days,

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
                    SUBSTR(ShipDate, 7, 4) || '-' ||
                    SUBSTR(ShipDate, 4, 2) || '-' ||
                    SUBSTR(ShipDate, 1, 2)
                )
            )
            AS INTEGER
        ) AS shipping_days,

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
        ) AS total_fulfillment_days

    FROM regional_sales
),

ranked_metrics AS (
    SELECT
        *,

        ROW_NUMBER() OVER (
            PARTITION BY SalesChannel
            ORDER BY total_fulfillment_days
        ) AS row_num,

        COUNT(*) OVER (
            PARTITION BY SalesChannel
        ) AS total_orders

    FROM fulfillment_metrics
    WHERE total_fulfillment_days IS NOT NULL
)

SELECT
    SalesChannel,
    total_orders,

    ROUND(AVG(processing_days), 2) AS average_processing_days,
    ROUND(AVG(shipping_days), 2) AS average_shipping_days,
    ROUND(AVG(total_fulfillment_days), 2) AS average_fulfillment_days,

    ROUND(
        AVG(
            CASE
                WHEN row_num IN (
                    (total_orders + 1) / 2,
                    (total_orders + 2) / 2
                )
                THEN total_fulfillment_days
            END
        ), 2
    ) AS median_fulfillment_days,

    MAX(
        CASE
            WHEN row_num = (total_orders * 9 + 9) / 10
            THEN total_fulfillment_days
        END
    ) AS p90_fulfillment_days

FROM ranked_metrics
GROUP BY SalesChannel, total_orders
ORDER BY average_fulfillment_days;


-- Query 4: Warehouse Fulfillment Analysis


WITH fulfillment_metrics AS (
    SELECT
        WarehouseCode,

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
        ) AS total_fulfillment_days

    FROM regional_sales
),

ranked_metrics AS (
    SELECT
        WarehouseCode,
        total_fulfillment_days,

        ROW_NUMBER() OVER (
            PARTITION BY WarehouseCode
            ORDER BY total_fulfillment_days
        ) AS row_num,

        COUNT(*) OVER (
            PARTITION BY WarehouseCode
        ) AS total_orders

    FROM fulfillment_metrics
    WHERE total_fulfillment_days IS NOT NULL
)

SELECT
    WarehouseCode,
    total_orders,

    ROUND(AVG(total_fulfillment_days), 2)
        AS average_fulfillment_days,

    ROUND(
        AVG(
            CASE
                WHEN row_num IN (
                    (total_orders + 1) / 2,
                    (total_orders + 2) / 2
                )
                THEN total_fulfillment_days
            END
        ), 2
    ) AS median_fulfillment_days,

    MAX(
        CASE
            WHEN row_num = (total_orders * 9 + 9) / 10
            THEN total_fulfillment_days
        END
    ) AS p90_fulfillment_days,

    MIN(total_fulfillment_days) AS minimum_days,
    MAX(total_fulfillment_days) AS maximum_days

FROM ranked_metrics
GROUP BY WarehouseCode, total_orders
ORDER BY average_fulfillment_days;


-- Query 5: Sales Team Fulfillment Analysis


WITH fulfillment_metrics AS (
    SELECT
        SalesTeamID,

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
        ) AS total_fulfillment_days

    FROM regional_sales
),

ranked_metrics AS (
    SELECT
        SalesTeamID,
        total_fulfillment_days,

        ROW_NUMBER() OVER (
            PARTITION BY SalesTeamID
            ORDER BY total_fulfillment_days
        ) AS row_num,

        COUNT(*) OVER (
            PARTITION BY SalesTeamID
        ) AS total_orders

    FROM fulfillment_metrics
    WHERE total_fulfillment_days IS NOT NULL
)

SELECT
    SalesTeamID,
    total_orders,

    ROUND(AVG(total_fulfillment_days), 2)
        AS average_fulfillment_days,

    ROUND(
        AVG(
            CASE
                WHEN row_num IN (
                    (total_orders + 1) / 2,
                    (total_orders + 2) / 2
                )
                THEN total_fulfillment_days
            END
        ), 2
    ) AS median_fulfillment_days,

    MAX(
        CASE
            WHEN row_num = (total_orders * 9 + 9) / 10
            THEN total_fulfillment_days
        END
    ) AS p90_fulfillment_days

FROM ranked_metrics
GROUP BY SalesTeamID, total_orders
ORDER BY average_fulfillment_days;


-- Query 6: Monthly Fulfillment Trends


WITH converted_dates AS (
    SELECT
        OrderNumber,

        SUBSTR(OrderDate, 7, 4) || '-' ||
        SUBSTR(OrderDate, 4, 2) AS order_month,

        DATE(
            SUBSTR(OrderDate, 7, 4) || '-' ||
            SUBSTR(OrderDate, 4, 2) || '-' ||
            SUBSTR(OrderDate, 1, 2)
        ) AS order_date,

        DATE(
            SUBSTR(DeliveryDate, 7, 4) || '-' ||
            SUBSTR(DeliveryDate, 4, 2) || '-' ||
            SUBSTR(DeliveryDate, 1, 2)
        ) AS delivery_date

    FROM regional_sales
),

monthly_metrics AS (
    SELECT
        order_month,
        COUNT(*) AS total_orders,

        AVG(
            JULIANDAY(delivery_date) -
            JULIANDAY(order_date)
        ) AS average_fulfillment_days

    FROM converted_dates
    WHERE order_month > '2018-05'
    GROUP BY order_month
),

monthly_growth AS (
    SELECT
        *,

        LAG(average_fulfillment_days) OVER (
            ORDER BY order_month
        ) AS previous_month_average

    FROM monthly_metrics
)

SELECT
    order_month,
    total_orders,

    ROUND(average_fulfillment_days, 2)
        AS average_fulfillment_days,

    ROUND(previous_month_average, 2)
        AS previous_month_average,

    ROUND(
        average_fulfillment_days - previous_month_average, 2
    ) AS change_in_days,

    ROUND(
        (
            average_fulfillment_days -
            previous_month_average
        ) * 100.0 /
        NULLIF(previous_month_average, 0), 2
    ) AS month_over_month_change_percentage

FROM monthly_growth
ORDER BY order_month;
