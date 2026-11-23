-- ==========================================
-- US REGIONAL SALES ANALYSIS
-- Module 01: Database Setup
-- ==========================================

-- Create the main sales table

CREATE TABLE IF NOT EXISTS regional_sales (
    OrderNumber TEXT PRIMARY KEY,
    SalesChannel TEXT,
    WarehouseCode TEXT,
    ProcuredDate TEXT,
    OrderDate TEXT,
    ShipDate TEXT,
    DeliveryDate TEXT,
    CurrencyCode TEXT,
    SalesTeamID INTEGER,
    CustomerID INTEGER,
    StoreID INTEGER,
    ProductID INTEGER,
    OrderQuantity INTEGER,
    DiscountApplied REAL,
    UnitCost REAL,
    UnitPrice REAL
);