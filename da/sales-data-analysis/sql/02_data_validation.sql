-- ==========================================
-- US REGIONAL SALES ANALYSIS
-- Module 02: Data Validation
-- ==========================================

-- 1. Total number of records
SELECT COUNT(*) AS total_records
FROM regional_sales;

-- 2. Check for duplicate order numbers
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT OrderNumber) AS unique_orders
FROM regional_sales;

-- 3. Inspect the table structure
PRAGMA table_info(regional_sales);

-- 4. Preview the first 5 records
SELECT *
FROM regional_sales
LIMIT 5;

-- 5. Check for missing values in important columns
SELECT
    SUM(CASE WHEN OrderNumber IS NULL THEN 1 ELSE 0 END) AS missing_order_numbers,
    SUM(CASE WHEN OrderQuantity IS NULL THEN 1 ELSE 0 END) AS missing_quantities,
    SUM(CASE WHEN UnitPrice IS NULL THEN 1 ELSE 0 END) AS missing_unit_prices,
    SUM(CASE WHEN UnitCost IS NULL THEN 1 ELSE 0 END) AS missing_unit_costs
FROM regional_sales;
