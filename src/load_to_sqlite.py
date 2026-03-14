import pandas as pd
import sqlite3

# Define the path to the raw data and the database
RAW_DATA_PATH = 'data/raw/telco_customer_churn.csv'
DB_PATH = 'database/telco_customer_churn.db'

# Read the raw data into a DataFrame
df = pd.read_csv(RAW_DATA_PATH)

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(DB_PATH)

# Write the DataFrame to a SQL table named 'raw_customer_churn'
df.to_sql('raw_customer_churn', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print(f"Data from {RAW_DATA_PATH} has been ingested into {DB_PATH} successfully.")