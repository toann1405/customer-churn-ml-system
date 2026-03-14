import sqlite3
import re

DB = 'database/telco_customer_churn.db'
SQL_FILE = 'sql/data_validation.sql'

with open(SQL_FILE, 'r', encoding='utf-8') as f:
    sql_text = f.read()

sql_text = re.sub(r"--.*", "", sql_text)
statements = [s.strip() for s in sql_text.split(';') if s.strip()]

conn = sqlite3.connect(DB)
cur = conn.cursor()

for i, stmt in enumerate(statements, start=1):
    if not stmt.lower().strip().startswith('select'):
        continue
    print(f"\n--- Statement {i}: {stmt.splitlines()[0].strip()} ---")
    cur.execute(stmt)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print(' | '.join(cols))
    for r in rows:
        print(' | '.join(str(x) for x in r))

conn.close()