import sqlite3

def run_sql_script(path):

    conn = sqlite3.connect("database/telco_customer_churn.db")
    cursor = conn.cursor()

    with open(path, "r") as file:
        sql = file.read()

    cursor.executescript(sql)

    conn.commit()
    conn.close()

    print(f"Executed {path}")


run_sql_script("sql/data_cleaning.sql")
run_sql_script("sql/feature_engineering.sql")
run_sql_script("sql/data_validation.sql")