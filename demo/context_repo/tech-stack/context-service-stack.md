---
type: tech-stack
id: ctx.tech.context-service-stack
title: Context Service Stack
description: Approved technical context for the demo application.
scope_id: context-studio-platform
durability: persistent
criticality: hybrid
status: approved
provenance: synthetic-demo/architecture-note
---

# Context Service Stack

The demo uses a Git-backed Markdown repository for governed Documents, SQLite for local app state and Collection indexes, FastAPI for the service layer, Astro for the CMS, and MCP tools for agent access.

## Retrieval Pattern

Agents should list scopes, types, folders, and indexes before reading full Documents. Collection semantic search is available only after a governed Document or folder surfaces the Collection as a supporting source.
