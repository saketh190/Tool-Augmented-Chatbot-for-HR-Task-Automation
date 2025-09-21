# tools/leave_tool.py
import os
POLICY_PATH = "D:/agent/Tool_Bot/policies.txt"
import sqlite3
from mcp.server.fastmcp import FastMCP

DB_PATH = "D:/agent/Tool_Bot/db/hr_leave.db"
POLICY_PATH = "D:/agent/Tool_Bot/policies.txt"

def load_policy():
    policy = {}
    if os.path.exists(POLICY_PATH):
        with open(POLICY_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    policy[key.strip()] = int(value.strip())
    return policy

def register_leave_tool(mcp: FastMCP):

    @mcp.tool()
    def apply_leave(emp_id: int, dates: list, reason: str):
        """
        Apply leave for one or more dates.
        Dates must be a list of YYYY-MM-DD strings.
        """
        policy = load_policy()
        if "max_annual_leaves" not in policy:
            return {"status": "failure", "message": "Policy not defined. Cannot apply leave."}
        max_leaves = policy["max_annual_leaves"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Pick year from the first date (assumes all in same year)
        year = dates[0].split("-")[0]

        # Count already taken this year
        cursor.execute(
            "SELECT COUNT(*) FROM leave_history WHERE emp_id=? AND leave_date LIKE ?",
            (emp_id, f"{year}-%")
        )
        taken = cursor.fetchone()[0]

        new_leaves = len(dates)
        if taken + new_leaves > max_leaves:
            conn.close()
            return {
                "status": "failure",
                "message": f"Cannot apply {new_leaves} more leaves. Already taken {taken}, max allowed {max_leaves}."
            }

        # Insert each leave date
        for d in dates:
            cursor.execute(
                "INSERT INTO leave_history (emp_id, leave_date, reason) VALUES (?, ?, ?)",
                (emp_id, d, reason)
            )

        conn.commit()
        conn.close()

        return {"status": "success", "message": f"{new_leaves} leave(s) applied for {emp_id}"}

    @mcp.tool()
    def get_leave_history(emp_id: int):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT leave_date, reason FROM leave_history WHERE emp_id=?", (emp_id,))
        rows = cursor.fetchall()
        conn.close()
        return {"emp_id": emp_id, "leaves": rows}
    
    @mcp.tool()
    def total_leaves(emp_id: int):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM leave_history WHERE emp_id=?", (emp_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return {"emp_id": emp_id, "total_leaves_taken": count}
    
    @mcp.tool()
    def list_employees():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, name, designation FROM employees")
        rows = cursor.fetchall()
        conn.close()
        employees = [{"emp_id": r[0], "name": r[1], "designation": r[2]} for r in rows]
        return {"employees": employees}
    
    @mcp.tool()
    def employee_details(emp_id: int):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, name, designation FROM employees WHERE emp_id=?", (emp_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"emp_id": row[0], "name": row[1], "designation": row[2]}
        else:
            return {"error": "Employee not found"}
    
    @mcp.tool()
    def cancel_leave(emp_id: int, date: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM leave_history WHERE emp_id=? AND leave_date=?",
            (emp_id, date)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        if affected > 0:
            return {"status": "success", "message": f"Leave on {date} for {emp_id} cancelled"}
        else:
            return {"status": "failure", "message": f"No leave found on {date} for {emp_id}"}
        
    @mcp.tool()
    def update_leave(emp_id: int, old_date: str, new_date: str, reason: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE leave_history SET leave_date=?, reason=? WHERE emp_id=? AND leave_date=?",
            (new_date, reason, emp_id, old_date)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        if affected > 0:
            return {"status": "success", "message": f"Leave updated from {old_date} to {new_date} for {emp_id}"}
        else:
            return {"status": "failure", "message": f"No leave found on {old_date} for {emp_id}"}
        
    @mcp.tool()
    def get_monthly_leaves(emp_id: int, month: int, year: int):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT leave_date, reason FROM leave_history WHERE emp_id=?",
            (emp_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        filtered = [ {"date": d, "reason": r} for d, r in rows if d.startswith(f"{year}-{month:02d}") ]
        return {"emp_id": emp_id, "month": month, "year": year, "leaves": filtered}

    @mcp.tool()
    def check_leave_on_date(emp_id: int, date: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT reason FROM leave_history WHERE emp_id=? AND leave_date=?",
            (emp_id, date)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"emp_id": emp_id, "date": date, "status": "on leave", "reason": row[0]}
        return {"emp_id": emp_id, "date": date, "status": "not on leave"}
    

