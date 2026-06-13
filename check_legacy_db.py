import sqlite3

conn = sqlite3.connect('legacy_teradata.db')
cursor = conn.cursor()

# Let's run a quick SQL query to see the first 5 rows of our "old" system
cursor.execute("SELECT * FROM raw_insurance_reporting LIMIT 5;")
rows = cursor.fetchall()

print("--- Data inside the Legacy Teradata System ---")
for row in rows:
    print(row)

conn.close()
