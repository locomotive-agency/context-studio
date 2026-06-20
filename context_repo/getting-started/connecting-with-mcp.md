---
type: reference
title: Connecting with MCP
description: How AI tools connect to the CMS through the MCP endpoint.
tags:
- getting-started
- mcp
- ai-tools
---

# Connecting with MCP

The CMS exposes valid context through MCP so AI tools can retrieve governed records instead of reading files directly.

## MCP URL

Local MCP endpoint:

```text
http://127.0.0.1:8001/mcp/
```

Hosted deployments should expose the same path on the hosted API domain:

```text
https://your-api-host.example.com/mcp/
```

## Available context operations

The MCP server exposes tools for:

- Retrieving records by type
- Searching context
- Assembling context packages for a task
- Validating available context

The same backend repository and OKF validation rules are used by the CMS and MCP service.

## Recommended connection pattern

1. Start or deploy the FastAPI service.
2. Confirm `/api/health` returns `status: ok`.
3. Add the `/mcp/` URL to the AI tool that supports MCP.
4. Request context by task, type, scope, or search query.

## Context quality

Only valid records should be used for governed context workflows. Use the Validation view in the CMS before relying on context from MCP.

## Scope-aware retrieval

Documents can include a `scope_id`. When a request includes scope, retrieval prefers the most specific matching context and can inherit from parent scopes.

This allows one repository to hold company, brand, product, campaign, audience, and channel context without duplicating every file.
