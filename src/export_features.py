import pandas as pd
import sqlite3

conn = sqlite3.connect("database/telco_customer_churn.db")

df = pd.read_sql(
    "SELECT * FROM final_features",
    conn
)

df.to_csv(
    "data/processed/churn_features.csv",
    index=False
)

print("Processed dataset exported")

conn.close()