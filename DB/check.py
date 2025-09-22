import sqlite3

DB_PATH = "D:/agent/Tool_Bot/db/hr_leave.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
