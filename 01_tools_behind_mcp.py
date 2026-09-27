"""Step 1 - the tool bodies the server exposes, run directly (no MCP runtime, no AI).

The MCP server is a thin wrapper: it advertises these functions to clients and forwards calls
to them. So before wiring up a client, confirm the actual work still does the right thing.
These are the same read-only functions from Episode 11.
"""
import _tools

print("get_service_status('checkout'):")
print(" ", _tools.get_service_status("checkout"))

print("\nget_metrics('nginx'):")
print(" ", _tools.get_metrics("nginx"))

print("\nhttp_check('https://shop.example.com/api/checkout'):")
print(" ", _tools.http_check("https://shop.example.com/api/checkout"))

print("\nThese are exactly what the MCP server exposes as tools. `mcp dev ops_mcp_server.py` "
      "lets you call them from the MCP Inspector; Claude Desktop can call them once installed.")
