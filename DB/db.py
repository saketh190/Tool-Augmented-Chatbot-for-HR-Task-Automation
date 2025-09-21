import sqlite3

# Connect to DB (or create new one)
conn = sqlite3.connect("hr_leave.db")
cursor = conn.cursor()

# Create employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    designation TEXT
)
""")

# Create leave history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_history (
    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id INTEGER,
    leave_date DATE,
    reason TEXT,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
)
""")

# Insert sample employees
employees = [
    (101, "Aditi Rao", "HR Executive"),
    (102, "Rohan Mehta", "Software Engg"),
    (103, "Priya Nair", "Data Analyst"),
    (104, "Arjun Singh", "Team Lead"),
    (105, "Neha Gupta", "DevOps Engg"),
    (106, "Vivek Shah", "Designer"),
    (107, "Kavya Iyer", "QA Engineer"),
    (108, "Manish Roy", "Product Mngr"),
    (109, "Sneha Das", "Backend Engg"),
    (110, "Rahul Verma", "Intern"),
]
cursor.executemany("INSERT OR IGNORE INTO employees VALUES (?, ?, ?)", employees)

# Insert leave history
leave_history = [
    (101, "2025-01-10", "Sick Leave"),
    (101, "2025-02-14", "Personal Work"),
    (102, "2025-01-05", "Family Function"),
    (102, "2025-03-21", "Medical"),
    (103, "2025-02-11", "Travel"),
    (104, "2025-01-20", "Sick Leave"),
    (104, "2025-03-01", "Personal Work"),
    (105, "2025-04-02", "Emergency"),
    (106, "2025-01-18", "Family Function"),
    (108, "2025-02-25", "Sick Leave"),
    (109, "2025-03-15", "Personal Work"),
    (110, "2025-04-10", "College Exam"),
]
cursor.executemany("INSERT INTO leave_history (emp_id, leave_date, reason) VALUES (?, ?, ?)", leave_history)

conn.commit()

# Example query: Get leave history for Rohan Mehta (emp_id=102)
cursor.execute("SELECT * FROM leave_history WHERE emp_id = 102")
print(cursor.fetchall())

conn.close()
