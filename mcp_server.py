from mcp.server.fastmcp import FastMCP
from tools.leave_tool import register_leave_tool
from tools.send_email_tool import register_send_email_tool
from tools.linkedin_tool import register_linkedin_tool
from tools.employee_tool import register_employee_tool  


mcp = FastMCP("HR Agent")
register_leave_tool(mcp)
register_send_email_tool(mcp)
register_linkedin_tool(mcp)
register_employee_tool(mcp)
# register_policy_tool(mcp) 

if __name__ == "__main__":
    mcp.run()
