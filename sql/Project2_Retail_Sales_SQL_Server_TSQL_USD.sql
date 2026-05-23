-- Project 2: Retail Sales Performance Analysis (USD)
-- SQL dialect: Microsoft SQL Server / T-SQL
-- Dataset: Synthetic retail sales data generated for portfolio use
-- Currency: USD ($)

CREATE DATABASE Project2_Retail_Sales_USD;
GO

USE Project2_Retail_Sales_USD;
GO

CREATE TABLE Fact_Sales (
    Order_ID VARCHAR(20),
    Order_Date DATE,
    Ship_Date DATE,
    Customer_ID VARCHAR(20),
    Customer_Name VARCHAR(150),
    Segment VARCHAR(50),
    Product_ID VARCHAR(20),
    Product_Name VARCHAR(150),
    Category VARCHAR(80),
    Subcategory VARCHAR(80),
    Province VARCHAR(80),
    Region_Group VARCHAR(50),
    City VARCHAR(80),
    Channel VARCHAR(80),
    Payment_Method VARCHAR(50),
    Ship_Mode VARCHAR(50),
    Quantity INT,
    Unit_Price_USD DECIMAL(12,2),
    Discount DECIMAL(6,4),
    Gross_Sales_USD DECIMAL(12,2),
    Discount_Amount_USD DECIMAL(12,2),
    Net_Sales_USD DECIMAL(12,2),
    Unit_Cost_USD DECIMAL(12,2),
    Total_Cost_USD DECIMAL(12,2),
    Profit_USD DECIMAL(12,2),
    Profit_Margin DECIMAL(8,4),
    Delivery_Days INT,
    Return_Status VARCHAR(30)
);
GO

-- After creating the table, import Fact_Sales.csv using SQL Server Import Wizard
-- or BULK INSERT after updating the file path.

-- 1. Overall KPI summary
SELECT
    SUM(Net_Sales_USD) AS total_net_sales_usd,
    SUM(Profit_USD) AS total_profit_usd,
    COUNT(DISTINCT Order_ID) AS total_orders,
    SUM(Quantity) AS quantity_sold,
    ROUND(SUM(Profit_USD) * 100.0 / NULLIF(SUM(Net_Sales_USD), 0), 2) AS profit_margin_percent,
    ROUND(SUM(Net_Sales_USD) * 1.0 / NULLIF(COUNT(DISTINCT Order_ID), 0), 2) AS average_order_value_usd,
    ROUND(SUM(CASE WHEN Return_Status = 'Returned' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(DISTINCT Order_ID), 0), 2) AS return_rate_percent
FROM Fact_Sales;

-- 2. Monthly sales and profit trend
SELECT
    DATETRUNC(month, Order_Date) AS sales_month,
    SUM(Net_Sales_USD) AS net_sales_usd,
    SUM(Profit_USD) AS profit_usd,
    COUNT(DISTINCT Order_ID) AS orders,
    SUM(Quantity) AS quantity_sold,
    ROUND(SUM(Profit_USD) * 100.0 / NULLIF(SUM(Net_Sales_USD), 0), 2) AS profit_margin_percent
FROM Fact_Sales
GROUP BY DATETRUNC(month, Order_Date)
ORDER BY sales_month;

-- 3. Sales and profit by category
SELECT
    Category,
    SUM(Net_Sales_USD) AS net_sales_usd,
    SUM(Profit_USD) AS profit_usd,
    COUNT(DISTINCT Order_ID) AS orders,
    SUM(Quantity) AS quantity_sold,
    ROUND(SUM(Profit_USD) * 100.0 / NULLIF(SUM(Net_Sales_USD), 0), 2) AS profit_margin_percent
FROM Fact_Sales
GROUP BY Category
ORDER BY net_sales_usd DESC;

-- 4. Top 10 products by net sales
SELECT TOP 10
    Product_Name,
    Category,
    SUM(Net_Sales_USD) AS net_sales_usd,
    SUM(Profit_USD) AS profit_usd,
    SUM(Quantity) AS quantity_sold,
    ROUND(SUM(Profit_USD) * 100.0 / NULLIF(SUM(Net_Sales_USD), 0), 2) AS profit_margin_percent
FROM Fact_Sales
GROUP BY Product_Name, Category
ORDER BY net_sales_usd DESC;

-- 5. Sales by channel
SELECT
    Channel,
    SUM(Net_Sales_USD) AS net_sales_usd,
    SUM(Profit_USD) AS profit_usd,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Profit_USD) * 100.0 / NULLIF(SUM(Net_Sales_USD), 0), 2) AS profit_margin_percent
FROM Fact_Sales
GROUP BY Channel
ORDER BY net_sales_usd DESC;

-- 6. Sales by customer segment
SELECT
    Segment,
    SUM(Net_Sales_USD) AS net_sales_usd,
    SUM(Profit_USD) AS profit_usd,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Profit_USD) * 100.0 / NULLIF(SUM(Net_Sales_USD), 0), 2) AS profit_margin_percent
FROM Fact_Sales
GROUP BY Segment
ORDER BY net_sales_usd DESC;

-- 7. Province performance
SELECT
    Province,
    Region_Group,
    SUM(Net_Sales_USD) AS net_sales_usd,
    SUM(Profit_USD) AS profit_usd,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Profit_USD) * 100.0 / NULLIF(SUM(Net_Sales_USD), 0), 2) AS profit_margin_percent
FROM Fact_Sales
GROUP BY Province, Region_Group
ORDER BY net_sales_usd DESC;

-- 8. Return analysis by category
SELECT
    Category,
    COUNT(DISTINCT Order_ID) AS orders,
    SUM(CASE WHEN Return_Status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    ROUND(SUM(CASE WHEN Return_Status = 'Returned' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(DISTINCT Order_ID), 0), 2) AS return_rate_percent
FROM Fact_Sales
GROUP BY Category
ORDER BY return_rate_percent DESC;

-- 9. Discount impact
SELECT
    Category,
    ROUND(AVG(Discount) * 100.0, 2) AS average_discount_percent,
    SUM(Discount_Amount_USD) AS discount_amount_usd,
    SUM(Net_Sales_USD) AS net_sales_usd,
    SUM(Profit_USD) AS profit_usd
FROM Fact_Sales
GROUP BY Category
ORDER BY discount_amount_usd DESC;
