# MCP

## Model Context Protocol

MCP provides a standardized tool/resource access layer for AI workflows.

## Project Structure

```text
backend/app/mcp/
├── __init__.py
├── client.py
├── filesystem.py
├── postgres.py
├── web.py
└── server.py
```

## Intended Flow

```text
AI Agent
   |
   v
MCP Client
   |
   +--> Web
   +--> Filesystem
   +--> PostgreSQL
   |
   v
Tool Result
   |
   v
Agent Reasoning
```

MCP separates agent reasoning from external tool access and makes integrations easier to extend.

Only claim a tool is actively used at runtime when the current agent/graph code actually invokes it.
