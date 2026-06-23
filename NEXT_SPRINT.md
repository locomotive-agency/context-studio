# Context System Organization Cleanup Sprint

**Goal:** Simplify `context_system/` around the current MCP retrieval model, remove construct-era remnants, and improve API organization without changing product behavior.

**Guardrails:**

- Follow `GOVERNANCE.md`.
- Keep business rules in services, persistence in repositories/stores, and UI formatting in the UI.
- Do not add backwards compatibility paths, deprecation layers, or versioned legacy endpoints.
- Do not add semantic retrieval over Documents.
- Keep changes small and testable.

## Evidence Preserved

- `resolve_criticality()` and `supporting_sources_for()` were unused outside `context_system/repository.py` and have been removed.
- `get_construct()` test usage was replaced with current APIs before removal.
- `/api/search`, `ContextService.search()`, `ContextRepository.search()`, and `SearchPointer` have been removed.
- `mcp_server.py` and `/api/mcp-tools/{tool_name}` now share `context_system/mcp_tools.py`.
- `app.py` now focuses on app construction, middleware, lifespan, health/stats, router registration, and MCP mount.
- Scope and schema behavior moved behind focused stores while `ContentStore` remains the public facade.

## Checklist

### 1. Remove Dead Construct/Search Code

- [x] Remove `ContextRepository.resolve_criticality()`.
- [x] Remove `ContextRepository.supporting_sources_for()`.
- [x] Replace test usage of `ContextRepository.get_construct()` with current APIs:
  - [x] Use `runtime_records()` where tests need raw runtime records.
  - [x] Use `ContextService.list_context_documents()` where tests need scoped metadata behavior.
- [x] Remove `ContextRepository.get_construct()`.
- [x] Remove `ContextRepository.search()`.
- [x] Remove `ContextService.search()`.
- [x] Remove `SearchPointer` from `models.py`.
- [x] Remove `/api/search`.
- [x] Remove or rewrite tests that assert legacy `/api/search` behavior.

### 2. Share MCP Tool Dispatch

- [x] Create one MCP tool registry used by both MCP and Tool Test Bench HTTP calls.
- [x] Move the `/api/mcp-tools/{tool_name}` dispatch table out of `app.py`.
- [x] Keep tool names aligned with the current contract:
  - [x] `list_context_scopes`
  - [x] `list_context_types`
  - [x] `list_context_folders`
  - [x] `read_context_index`
  - [x] `read_context_log`
  - [x] `list_context_documents`
  - [x] `read_context_document`
  - [x] `search_collection`
  - [x] `read_collection_source`
  - [x] `validate_context`
- [x] Confirm MCP and Tool Test Bench call the same service methods.

### 3. Add Typed API Boundaries

- [x] Add Pydantic request models for MCP tool calls.
- [x] Add Pydantic request models for OKF folder import endpoints.
- [x] Add Pydantic request models for Collection create/upload endpoints.
- [x] Replace raw `dict` endpoint payloads where validation affects behavior.
- [x] Keep error messages clear and plain.

### 4. Split FastAPI Routes

- [x] Create route modules for auth/users.
- [x] Create route modules for documents/folders/schemas/scopes.
- [x] Create route modules for imports.
- [x] Create route modules for collections.
- [x] Create route module for MCP tool test endpoints.
- [x] Keep `app.py` focused on app construction, middleware, lifespan, and router registration.
- [x] Preserve existing endpoint paths unless removing legacy search endpoints.

### 5. Tidy Store Boundaries

- [x] Identify a low-risk split for `ContentStore`.
- [x] Move scope hierarchy behavior into a focused scope store or helper.
- [x] Move schema merge/read/write behavior into a focused schema store or helper.
- [x] Keep `ContentStore` as a facade until callers are migrated.
- [x] Do not rewrite collection indexing in this sprint unless tests require it.

### 6. Verification

- [x] Run `uv run pytest`.
- [x] Run `npm run build` from `cms/` if frontend-facing code changes.
- [x] Run `git diff --check`.
- [x] Confirm Tool Test Bench still lists and runs all MCP tools.
- [x] Confirm no Document semantic search endpoint remains.
- [x] Confirm Collections search still works through `search_collection()`.
