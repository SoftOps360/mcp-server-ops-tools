"""ops-tools MCP server - expose our READ-ONLY ops tools over the Model Context Protocol,
so ANY MCP client (Claude Desktop, an IDE, our own agent) can use them - no custom glue per client.

MCP is an open protocol, not a product: you write a server once, and every MCP-speaking client
can call its tools. Here we wrap the exact same read-only functions from Episode 11.

Run / connect:
    pip install "mcp[cli]"
    mcp dev ops_mcp_server.py        # opens the MCP Inspector to try the tools
    mcp install ops_mcp_server.py    # registers it with Claude Desktop (see claude_desktop_config.json)

Everything here is READ-ONLY. Exposing write actions over MCP is possible, but they must sit
behind the Episode 13 guardrails first - never hand a client unguarded write access.
"""
from mcp.server.fastmcp import FastMCP
import _tools

mcp = FastMCP("ops-tools")


@mcp.tool()
def get_service_status(service: str) -> dict:
    """Current status of a service: replicas, image, last event. Read-only."""
    return _tools.get_service_status(service)


@mcp.tool()
def tail_logs(service: str, lines: int = 20) -> dict:
    """Last N log lines for a service. Read-only."""
    return _tools.tail_logs(service, lines)


@mcp.tool()
def get_metrics(service: str) -> dict:
    """Current metrics for a service: cpu, mem, error_rate, p95, throughput. Read-only."""
    return _tools.get_metrics(service)


@mcp.tool()
def http_check(url: str) -> dict:
    """Read-only HTTP GET health check of a URL -> status code."""
    return _tools.http_check(url)


if __name__ == "__main__":
    # Default transport is stdio, which is what Claude Desktop and `mcp dev` use.
    mcp.run()
