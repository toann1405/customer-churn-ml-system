DROP TABLE IF EXISTS cleaned_churn;
CREATE TABLE cleaned_churn AS
SELECT "CustomerID" AS customerID,
    "Gender" AS gender,
    "Senior Citizen" AS SeniorCitizen,
    "Partner" AS Partner,
    "Dependents" AS Dependents,
    CAST("Tenure Months" AS INTEGER) AS tenure,
    "Phone Service" AS PhoneService,
    "Multiple Lines" AS MultipleLines,
    "Internet Service" AS InternetService,
    "Online Security" AS OnlineSecurity,
    "Online Backup" AS OnlineBackup,
    "Device Protection" AS DeviceProtection,
    "Tech Support" AS TechSupport,
    "Streaming TV" AS StreamingTV,
    "Streaming Movies" AS StreamingMovies,
    "Contract" AS Contract,
    "Paperless Billing" AS PaperlessBilling,
    "Payment Method" AS PaymentMethod,
    CAST("Monthly Charges" AS FLOAT) AS MonthlyCharges,
    CASE
        WHEN "Total Charges" = '' THEN NULL
        ELSE CAST("Total Charges" AS FLOAT)
    END AS TotalCharges,
    "Churn Value" AS Churn
FROM raw_customer_churn
WHERE "Monthly Charges" IS NOT NULL;