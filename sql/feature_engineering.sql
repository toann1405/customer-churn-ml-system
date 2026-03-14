DROP TABLE IF EXISTS final_features;
CREATE TABLE final_features AS
SELECT *,
    -- Feature 1: tenure groups
    CASE
        WHEN tenure <= 12 THEN 'New'
        WHEN tenure <= 24 THEN 'Regular'
        WHEN tenure <= 48 THEN 'Loyal'
        ELSE 'Very Loyal'
    END AS tenure_group,
    -- Feature 2: total services count
    (
        CASE
            WHEN OnlineSecurity = 'Yes' THEN 1
            ELSE 0
        END + CASE
            WHEN OnlineBackup = 'Yes' THEN 1
            ELSE 0
        END + CASE
            WHEN DeviceProtection = 'Yes' THEN 1
            ELSE 0
        END + CASE
            WHEN TechSupport = 'Yes' THEN 1
            ELSE 0
        END + CASE
            WHEN StreamingTV = 'Yes' THEN 1
            ELSE 0
        END + CASE
            WHEN StreamingMovies = 'Yes' THEN 1
            ELSE 0
        END
    ) AS total_services_count,
    -- Feature 3: average monthly spending
    CASE
        WHEN tenure > 0 THEN TotalCharges / tenure
        ELSE NULL
    END AS avg_monthly_spending,
    -- Feature 4: Bill Shock / Spending Spike (Was found from EDA)
    MonthlyCharges - (
        CASE
            WHEN tenure > 0 THEN TotalCharges / tenure
            ELSE MonthlyCharges
        END
    ) AS spending_spike
FROM cleaned_churn;