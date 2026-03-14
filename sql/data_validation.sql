-- ==========================================
-- DATA QUALITY TESTS
-- All tests should return Defect_Count = 0
-- ==========================================

-- Test 1: Duplicate customerID
SELECT 
    'Duplicate CustomerID' AS Test_Name,
    COUNT(*) - COUNT(DISTINCT customerID) AS Defect_Count
FROM final_features;

-- Test 2: Invalid NULL TotalCharges
SELECT 
    'Invalid NULL TotalCharges' AS Test_Name,
    COUNT(*) AS Defect_Count
FROM final_features
WHERE TotalCharges IS NULL 
AND tenure > 0;

-- Test 3: Negative MonthlyCharges
SELECT
    'Negative MonthlyCharges' AS Test_Name,
    COUNT(*) AS Defect_Count
FROM final_features
WHERE MonthlyCharges < 0;

-- Test 4: Negative avg_monthly_spending
SELECT 
    'Negative avg_monthly_spending' AS Test_Name,
    COUNT(*) AS Defect_Count
FROM final_features
WHERE avg_monthly_spending < 0;

-- Test 5: Invalid service count
SELECT
    'Invalid total_services_count' AS Test_Name,
    COUNT(*) AS Defect_Count
FROM final_features
WHERE total_services_count < 0
OR total_services_count > 6;


-- ==========================================
-- DATA DISTRIBUTION CHECKS (Profiling)
-- ==========================================

-- Churn distribution
SELECT 
    Churn AS Target_Class,
    COUNT(*) AS Total_Customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM final_features), 2) AS Percentage
FROM final_features
GROUP BY Churn;

-- Tenure group distribution
SELECT
    tenure_group,
    COUNT(*) AS Total_Customers
FROM final_features
GROUP BY tenure_group;