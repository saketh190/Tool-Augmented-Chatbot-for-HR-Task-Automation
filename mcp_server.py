from mcp.server.fastmcp import FastMCP
from tools.leave_tool import register_leave_tool

mcp = FastMCP("HR Agent")
register_leave_tool(mcp)

if __name__ == "__main__":
    # Remove prints to avoid breaking MCP handshake for Claude
    # print("🟢 HR Agent MCP Server is starting...")
    mcp.run()  # Use default port 3333, no arguments