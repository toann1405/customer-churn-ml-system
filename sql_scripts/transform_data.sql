DROP TABLE IF EXISTS cleaned_churn;
CREATE TABLE cleaned_churn AS
SELECT DISTINCT TRIM("CustomerID") AS customerID,
    "Gender" AS gender,
    "Senior Citizen" AS SeniorCitizen,
    "Partner" AS Partner,
    "Dependents" AS Dependents,
    CAST("Tenure Months" AS INTEGER) AS tenure,
    "Phone Service" AS PhoneService,
    CASE
        WHEN "Multiple Lines" IN ('No phone service', 'No') THEN 'No'
        ELSE "Multiple Lines"
    END AS MultipleLines,
    "Internet Service" AS InternetService,
    CASE
        WHEN "Online Security" = 'No internet service' THEN 'No'
        ELSE "Online Security"
    END AS OnlineSecurity,
    CASE
        WHEN "Online Backup" = 'No internet service' THEN 'No'
        ELSE "Online Backup"
    END AS OnlineBackup,
    CASE
        WHEN "Device Protection" = 'No internet service' THEN 'No'
        ELSE "Device Protection"
    END AS DeviceProtection,
    CASE
        WHEN "Tech Support" = 'No internet service' THEN 'No'
        ELSE "Tech Support"
    END AS TechSupport,
    CASE
        WHEN "Streaming TV" = 'No internet service' THEN 'No'
        ELSE "Streaming TV"
    END AS StreamingTV,
    CASE
        WHEN "Streaming Movies" = 'No internet service' THEN 'No'
        ELSE "Streaming Movies"
    END AS StreamingMovies,
    "Contract" AS Contract,
    "Paperless Billing" AS PaperlessBilling,
    "Payment Method" AS PaymentMethod,
    CAST("Monthly Charges" AS FLOAT) AS MonthlyCharges,
    CASE
        WHEN "Total Charges" = ''
        OR "Total Charges" = ' '
        OR "Total Charges" IS NULL THEN 0.0
        ELSE CAST("Total Charges" AS FLOAT)
    END AS TotalCharges,
    CAST("Churn Value" AS INTEGER) AS Churn
FROM raw_customer_churn
WHERE "CustomerID" IS NOT NULL
    AND "CustomerID" != ''
    AND "Monthly Charges" IS NOT NULL
    AND CAST("Tenure Months" AS INTEGER) >= 0;