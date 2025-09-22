import sqlite3
import os

DB_PATH = "d:/agent/Tool_Bot/DB/hr_leave.db"
EMPLOYEE_MODIFY_PASSWORD = os.getenv("EMPLOYEE_MODIFY_PASSWORD")

def get_employee_detail(emp_id=None, name=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if emp_id:
        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
    elif name:
        cursor.execute("SELECT * FROM employees WHERE name = ?", (name,))
    else:
        conn.close()
        return "Please provide either emp_id or name."
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            "emp_id": result[0],
            "name": result[1],
            "designation": result[2],
            "email": result[3]
        }
    else:
        return "Employee not found."

def create_employee(name, designation, email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, designation, email) VALUES (?, ?, ?)",
        (name, designation, email)
    )
    conn.commit()
    emp_id = cursor.lastrowid
    conn.close()
    return f"Employee created successfully with emp_id {emp_id}."

def delete_employee(emp_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted:
        return "Employee deleted successfully."
    else:
        return "Employee not found."

def modify_employee(emp_id, name=None, designation=None, email=None, password=None):
    if not password or password != EMPLOYEE_MODIFY_PASSWORD:
        return "Invalid password. Modification not allowed."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    updates = []
    params = []
    if name:
        updates.append("name = ?")
        params.append(name)
    if designation:
        updates.append("designation = ?")
        params.append(designation)
    if email:
        updates.append("email = ?")
        params.append(email)
    if not updates:
        conn.close()
        return "No fields to update."
    params.append(emp_id)
    sql = f"UPDATE employees SET {', '.join(updates)} WHERE emp_id = ?"
    cursor.execute(sql, params)
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated:
        return "Employee details updated successfully."
    else:
        return "Employee not found."

def register_employee_tool(mcp):
    @mcp.tool(
        "get_employee_detail",
        description="Fetch details of an employee by emp_id or name."
    )
    def get_employee_detail_tool(emp_id: int = None, name: str = None):
        return get_employee_detail(emp_id, name)

    @mcp.tool(
        "create_employee",
        description="Create a new employee with name, designation, and email. emp_id is auto-incremented."
    )
    def create_employee_tool(name: str, designation: str, email: str):
        return create_employee(name, designation, email)

    @mcp.tool(
        "delete_employee",
        description="Delete an employee by emp_id."
    )
    def delete_employee_tool(emp_id: int):
        return delete_employee(emp_id)

    @mcp.tool(
        "modify_employee",
        description="Modify employee details (name, designation, email) by emp_id. Requires password."
    )
    def modify_employee_tool(emp_id: int, name: str = None, designation: str = None, email: str = None, password: str = None):
        """
        Modify employee details.
        Args:
            emp_id (int): Employee ID.
            name (str, optional): New name.
            designation (str, optional): New designation.
            email (str, optional): New email.
            password (str): Security password.
        Returns:
            str: Status message.
        """
        return modify_employee(emp_id, name, designation, email, password)