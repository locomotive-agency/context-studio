# Prototype Architecture

## Components

The prototype keeps six logical components in one deployable application:

1. Document database: OKF Markdown records and JSON source documents under `context_repo/` in the project Git repository.
2. Schema model: Pydantic record models, inherited `_schema.yaml` governance, and the `_scopes.yaml` hierarchy.
3. CMS: Astro document, scope, schema, history, validation, and user management with RBAC.
4. Context service: FastAPI and FastMCP retrieval, import, package assembly, and management endpoints, mounted at `/mcp/`.
5. Collections: local buckets of stored source files under `var/collections/`, indexed in SQLite for supporting retrieval.
6. Tool Test Bench: CMS screen that calls the real context package endpoint so users can inspect what an AI workflow would receive.

Keeping these as code boundaries rather than separate deployments avoids unnecessary operational complexity.

The custom Astro CMS is the documentation layer. GitBook and Docusaurus are not dependencies. SQLite is used for users, sessions, audit events, Collections, and other local state that does not belong in versioned OKF documents.

## Format Rules

The bundle follows OKF draft v0.1: UTF-8 Markdown concept files with YAML frontmatter and a required non-empty `type`. `index.md` and `log.md` remain reserved. Producer-defined governance fields are preserved.

Folder schemas are a system convention layered on OKF. Schemas merge from the bundle root toward the document's folder. Document frontmatter has final precedence.

Each governed record may reference one `scope_id`. Scope nodes use parent relationships. Retrieval includes records assigned to the requested scope or its ancestors, then returns records at the most specific matching level for each construct.

Governance metadata should stay minimal. Do not add `owner_role`, `approver_role`, `audit_required`, `source_refs`, `retrieval_policy`, `exact_language_required`, or similar per-record workflow fields back into the model. Use the existing axes: `criticality`, `status`, `durability`, `scope_id`, `provenance`, `valid_until`, and `edit_roles` only if lightweight folder or document edit hints are still useful. Runtime audit should be service behavior, not per-record metadata.

Documents and folders may define supporting-source pointers for hybrid and flexible context:

```yaml
supporting_sources:
  collections:
    - collection-1
    - collection-2
  web:
    - https://example.com/page
  mcp:
    - sales-calls
    - https://example.com/mcp
```

These pointers are not canonical truth. Controlled context ignores them. MCP sources require authenticated access before being returned.

Repository history shows structural and application changes. Document history filters the same Git graph by file path. Markdown and JSON editors share Raw, Preview, and Split views.

## Retrieval Rules

- Invalid OKF documents remain visible in the CMS validation report.
- Invalid documents are excluded from search, context packages, and MCP retrieval.
- OKF documents use deterministic retrieval only.
- Controlled requests return approved OKF records or block when required context is missing.
- Controlled requests never search Collections, web pointers, or MCP pointers.
- Hybrid and flexible requests return approved OKF records when available.
- Hybrid and flexible requests may search only the Collections named by matching OKF document or folder supporting-source pointers.
- Collection retrieval combines SQLite FTS5 keyword matching with a local deterministic embedding vector and returns cited passages.
- Collection files are never summarized and are never promoted into OKF records automatically.

## Current Sprint State

The current sprint is implemented in code and CMS surfaces:

- Context package v1 contract at `/api/context-package`.
- OKF folder import scan/apply endpoints and CMS import panel.
- Collections storage, source document retention, MarkItDown parsing path, retrieval units, FTS index, embedding table, and cited retrieval.
- Supporting-source pointers for documents and folder schemas.
- MCP supporting-source authentication filtering.
- Tool Test Bench CMS screen that calls the real context package endpoint.
- Backend tests covering controlled blocking, Collection routing, MCP source filtering, OKF import, no OKF semantic retrieval, and no Collection summarization API.

The next implementation priority is user permissions.

## Roadmap

### 1. User permissions

The next step is to make the app, API, MCP server, CMS controls, and tests follow the same permissions.

Goals:

- All access requires login through local username/password or GitHub.
- Admins can edit users and everything else.
- Editors can edit Folders, Documents, and Collections.
- Viewers can request context and semantic data.

Implementation shape:

- Add direct route-level tests for missing-login, Viewer, Editor, and Admin behavior.
- Require logged-in user context for API and MCP data access.
- Align Folder, Document, and Collection write permissions with the Editor role.
- Keep user management admin-only.
- Make CMS controls match the same permissions as the API.

### 2. Productionize Collection Retrieval

The current Collection retrieval implementation is local and deterministic. It establishes the product boundary and citation behavior without introducing remote infrastructure.

Next improvements:

- Add an adapter for a stronger local embedding model.
- Add an adapter for a local vector store if the deterministic embedding table becomes too limited.
- Add indexing progress for large file batches.
- Add reindex controls for individual documents and whole Collections.
- Keep all usage routing in OKF supporting-source pointers, not Collection metadata.

### 3. MCP Source Registry

Supporting-source metadata can point to MCP servers. The next step is a small registry of supported MCP servers and access policy.

Next improvements:

- Add config validation for MCP server IDs and URLs.
- Show unavailable MCP sources clearly in the Tool Test Bench.
- Keep MCP references at the server level, not the tool level.

## Sources

- Astro getting started: https://docs.astro.build/en/getting-started/
- Astro endpoints: https://docs.astro.build/en/guides/endpoints/
- OKF v0.1 draft: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/2d0bb3f547b847fcbd1c7611bdab8a9e2ccb098f/okf/SPEC.md
- MCP Python SDK streamable HTTP mounting: https://github.com/modelcontextprotocol/python-sdk
