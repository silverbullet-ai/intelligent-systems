
-- ============================================================
-- US REGIONAL SALES ANALYSIS
-- File: test.sql
-- Purpose: Exploratory queries, debugging and QA validation
-- ============================================================

-- ============================================================
-- MODULE REFERENCE INDEX
-- ============================================================
--
-- Module 01: Database Setup
-- Module 02: Data Validation
-- Module 03: Overall Performance Analysis
-- Module 04: Sales Channel Analysis
-- Module 05: Monthly Sales Analysis
-- Module 06: Warehouse Performance Analysis
-- Module 07: Product Performance Analysis
-- Module 08: Customer Performance Analysis
-- Module 09: Sales Team Performance Analysis
-- Module 10: Store Performance Analysis
-- Module 11: Discount & Profitability Analysis
-- Module 12: Fulfillment Analysis
-- Module 13: Business Insights
--
-- ============================================================


-- ============================================================
-- SECTION 1: GENERAL DATA INSPECTION
-- Related to: Initial project setup and data validation
-- ============================================================

-- Query 1.1: Inspect monetary columns and calculations

SELECT
    OrderNumber,
    OrderQuantity,
    UnitCost,
    UnitPrice,
    OrderQuantity * UnitPrice AS gross_sales,
    OrderQuantity * UnitCost AS total_cost
FROM regional_sales
LIMIT 5;


-- Query 1.2: Inspect date formats

SELECT
    OrderDate,
    ProcuredDate,
    ShipDate,
    DeliveryDate
FROM regional_sales
LIMIT 10;


-- ============================================================
-- SECTION 2: FLOATING-POINT PRECISION INVESTIGATION
-- Related to: Modules 07, 08, 09, 10 and 11
-- ============================================================

-- Query 2.1: Identify near-zero negative profits
-- Investigates negative profits that become zero after
-- rounding to two decimal places.

WITH order_profit AS (
    SELECT
        OrderNumber,
        ProductID,
        (
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) AS profit
    FROM regional_sales
)

SELECT
    OrderNumber,
    ProductID,
    ROUND(profit, 6) AS calculated_profit,
    ROUND(profit, 2) AS rounded_profit
FROM order_profit
WHERE profit < 0
  AND ROUND(profit, 2) = 0
ORDER BY profit DESC;


-- Query 2.2: Inspect full floating-point precision

WITH order_profit AS (
    SELECT
        OrderNumber,
        ProductID,
        (
            OrderQuantity * UnitPrice * (1 - DiscountApplied)
            - OrderQuantity * UnitCost
        ) AS profit
    FROM regional_sales
)

SELECT
    OrderNumber,
    ProductID,
    printf('%.15f', profit) AS precise_profit
FROM order_profit
WHERE profit < 0
  AND ROUND(profit, 2) = 0
ORDER BY profit DESC;


-- ============================================================
-- SECTION 3: PYTHON AND SQL RECONCILIATION
-- Related to: Module 07 - Product Performance Analysis
-- Also used for: Overall project validation
-- ============================================================

-- Query 3.1: Reproduce Python's business metric calculation
-- sequence to ensure consistent loss-making order classification.

WITH calculated_metrics AS (
    SELECT
        OrderNumber,
        ProductID,

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
        ProductID,
        net_sales - total_cost AS profit
    FROM calculated_metrics
)

SELECT
    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN profit < 0 THEN 1
            ELSE 0
        END
    ) AS loss_making_orders,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN profit < 0 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS loss_percentage

FROM order_profit;


-- ============================================================
-- SECTION 4: MODULE 10 - STORE PERFORMANCE ANALYSIS
-- ============================================================

-- Query 4.1: Validate loss-making order count and
-- the number of stores associated with those orders.

WITH calculated_metrics AS (
    SELECT
        OrderNumber,
        StoreID,

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
)

SELECT
    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN profit < 0 THEN 1
            ELSE 0
        END
    ) AS loss_making_orders,

    COUNT(
        DISTINCT CASE
            WHEN profit < 0 THEN StoreID
        END
    ) AS stores_with_losses

FROM order_profit;


-- ============================================================
-- SECTION 5: MODULE 12 & 13 - FINAL VALIDATION
-- ============================================================

-- Query 5.1: December 2020 final validation
-- Module 12: Fulfillment Analysis
-- Module 13: Business Insights
--
-- Validate December 2020 order count, average order profit,
-- and average fulfillment time.

SELECT
    COUNT(*) AS total_orders,

    ROUND(
        AVG(
            (
                (OrderQuantity * UnitPrice)
                - ((OrderQuantity * UnitPrice) * DiscountApplied)
            ) - (OrderQuantity * UnitCost)
        ),
        2
    ) AS average_order_profit,

    ROUND(
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
        ),
        2
    ) AS average_fulfillment_days

FROM regional_sales

WHERE
    SUBSTR(OrderDate, 7, 4) || '-' ||
    SUBSTR(OrderDate, 4, 2) = '2020-12';


-- ============================================================
-- END OF EXPLORATORY AND VALIDATION QUERIES
-- ============================================================
