-- Retail Sales Analytics SQL Queries

-- 1. Total revenue
SELECT SUM(Quantity * Unit_Price) AS total_revenue
FROM sales_data;

-- 2. Revenue by category
SELECT Category, SUM(Quantity * Unit_Price) AS revenue
FROM sales_data
GROUP BY Category
ORDER BY revenue DESC;

-- 3. Revenue by region
SELECT Region, SUM(Quantity * Unit_Price) AS revenue
FROM sales_data
GROUP BY Region
ORDER BY revenue DESC;

-- 4. Top 10 products
SELECT Product,
       SUM(Quantity) AS units_sold,
       SUM(Quantity * Unit_Price) AS revenue
FROM sales_data
GROUP BY Product
ORDER BY revenue DESC
LIMIT 10;

-- 5. Monthly revenue
SELECT strftime('%Y-%m', Date) AS month,
       SUM(Quantity * Unit_Price) AS revenue
FROM sales_data
GROUP BY month
ORDER BY month;

-- 6. Customer order count
SELECT Customer_ID,
       COUNT(DISTINCT Order_ID) AS orders
FROM sales_data
GROUP BY Customer_ID
ORDER BY orders DESC;
