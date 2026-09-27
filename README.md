# Episode 14 — Write an MCP Server for your Ops Tools

We built ops tools and wired them into our own agent. But what if you want the **same tools**
usable from Claude Desktop, an IDE, *and* your agent — without re-gluing them into each one?
That's what **MCP (Model Context Protocol)** is for: write the tools as a **server once**, and
every MCP-speaking client can call them.

## What MCP actually is (kills two myths)

> **MCP is an open protocol — a standard way for an AI client to discover and call your tools.**

- *"MCP is a product / a company's thing."* No — it's an **open protocol**. Your server works
  with any client that speaks it.
- *"MCP is only for coding assistants."* No — a tool is a tool. Here we expose **ops** tools
  (service status, logs, metrics, health checks).

The split matters: an **MCP server has no LLM of its own.** The LLM lives in the **client**
(Claude Desktop, an IDE, or your agent). The server just advertises tools and runs them when asked.

## Files

| File | What it is |
|------|-----------|
| `ops_mcp_server.py` | The MCP server — wraps the read-only tools with `FastMCP` + `@mcp.tool()`. |
| `_tools.py`, `sample_ops/` | The same read-only tools + incident from Episode 11. |
| `01_tools_behind_mcp.py` | Run the tool bodies directly (no MCP runtime) to confirm the work. |
| `claude_desktop_config.json` | Example config to register the server with Claude Desktop. |

## Setup

```bash
pip install "mcp[cli]"
```

## Try it three ways

**1) The MCP Inspector (fastest):**
```bash
mcp dev ops_mcp_server.py
```
Opens a local UI where you can see the four tools and call them by hand.

**2) In Claude Desktop:**
```bash
mcp install ops_mcp_server.py        # auto-adds the entry, or edit the file below yourself
```
Or hand-edit `%APPDATA%\Claude\claude_desktop_config.json` (macOS:
`~/Library/Application Support/Claude/claude_desktop_config.json`) using
`claude_desktop_config.json` here as a template, then **fully restart Claude Desktop**. Ask it
*"what's the status of the checkout service?"* and it will call your tool.

**3) From your own agent:** point an MCP client at the same server — the tools are identical to
the ones the Episode 11–13 agent used, now reachable over the protocol.

## The read-only line still holds

Every tool exposed here is **read-only**. You *can* expose write actions over MCP, but they must
sit **behind the Episode 13 guardrails** (approval, blast-radius, deny-list, audit) first. A tool
reachable by any client is a bigger attack surface, not a smaller one — never expose an unguarded
write. (Prompt-injection risk once a client has tools is covered in Episode 21.)

## How it was verified

`mcp` isn't installed in the authoring sandbox, so the server's transport isn't run here. What is
verified: the server **compiles** (the FastMCP wiring is standard), the Claude Desktop config is
**valid JSON**, and the **tool bodies run correctly** on the sample incident (`01_tools_behind_mcp.py`
— checkout `crashed`/`OOMKilled`, nginx 68% errors, `502` on `/api/checkout`). Install `mcp[cli]`
and run `mcp dev ops_mcp_server.py` to exercise the live protocol.

## Honesty & limits (please keep these in the video)

- **The tools are simulated over `sample_ops/`** so it runs offline. Point them at real read-only
  commands/APIs in `_tools.py`; the MCP layer doesn't change.
- **MCP details evolve.** The SDK, the `mcp` CLI flags, and the Claude Desktop config path can
  change between versions — check the current MCP docs if a command differs.
- **A server is a boundary you own.** Only expose what you intend to; least privilege applies to
  MCP tools exactly like it does to the agent's own tools.
