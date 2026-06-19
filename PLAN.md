# Prototype Architecture

## Components

The prototype keeps five logical components in one deployable application:

1. OKF document database: Markdown concepts in the local Git repository under `context_repo/`.
2. Schema model: Pydantic record models, inherited `_schema.yaml` governance, and the `_scopes.yaml` hierarchy.
3. CMS: Astro document, scope, schema, history, validation, and user management with RBAC.
4. Context service: FastAPI and FastMCP retrieval and management endpoints, mounted at `/mcp/`.
5. Unstructured retrieval: local lexical search over valid flexible and hybrid documents. This is the prototype boundary for a future semantic retrieval implementation; it is not embedding-based today.

Keeping these as code boundaries rather than separate deployments avoids unnecessary operational complexity.

## Format Rules

The bundle follows OKF draft v0.1: UTF-8 Markdown concept files with YAML frontmatter and a required non-empty `type`. `index.md` and `log.md` remain reserved. Producer-defined governance fields are preserved.

Folder schemas are a system convention layered on OKF. Schemas merge from the bundle root toward the document's folder. Document frontmatter has final precedence.

Each governed record may reference one `scope_id`. Scope nodes use parent relationships. Retrieval includes records assigned to the requested scope or its ancestors, then returns records at the most specific matching level for each construct.

## Retrieval Rules

- Invalid OKF documents remain visible in the CMS validation report.
- Invalid documents are excluded from search, context packages, and MCP retrieval.
- Controlled documents use deterministic retrieval and audit logging.
- Hybrid and flexible documents can use local text search.

## Sources

- Astro getting started: https://docs.astro.build/en/getting-started/
- Astro endpoints: https://docs.astro.build/en/guides/endpoints/
- OKF v0.1 draft: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/2d0bb3f547b847fcbd1c7611bdab8a9e2ccb098f/okf/SPEC.md
- MCP Python SDK streamable HTTP mounting: https://github.com/modelcontextprotocol/python-sdk
