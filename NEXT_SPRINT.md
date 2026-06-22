# Governed MCP Retrieval And Tool Test Bench Sprint Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Follow the checkbox order and update this file as each task is completed.

**Goal:** Rework MCP and Tool Test Bench so agents discover governed context progressively, retrieve full text only when needed, and search Collections only through Document-declared supporting sources.

**Architecture:** Documents remain deterministic OKF records governed by `type`, `scope_id`, folder schema, status, criticality, and Git history. Collections remain supporting source buckets and are searchable only when an in-scope Document or folder schema points to them through `supporting_sources.collections`. Tool Test Bench should exercise the same service paths MCP uses.

**Tech Stack:** FastAPI, FastMCP, Pydantic, SQLite FTS5 Collections, Git-backed OKF repository, Astro CMS, pytest.

---

## Sources Reviewed

- `README.md`
- `GOVERNANCE.md`
- Archived sprint plan: `archive/2026-06-22-okf-and-mcp-agent-retrieval-alignment.md`
- Karpathy LLM wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Google OKF spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- Current implementation in `context_system/app.py`, `context_system/mcp_server.py`, `context_system/service.py`, `context_system/repository.py`, `context_system/cms.py`, `context_system/okf.py`, `context_system/models.py`, `context_system/collections.py`, and `cms/src/pages/index.astro`

## Design Rules

- Do not add `tags` to the new MCP discovery contract. We should rely on `type`, `scope_id`, folder path, status, criticality, and supporting source pointers.
- Do not run semantic retrieval over Documents.
- Do not return full Document body text from aggregate discovery tools.
- Do allow full Document body text through an explicit read tool.
- Do allow Collection search only for Collections surfaced from a scoped Document or folder response.
- Do not expose absolute server filesystem paths through MCP or Tool Test Bench responses.
- Do not add `scope_mode`. Scope behavior should follow the existing scope hierarchy and server-side visibility checks.
- Use Git as the authoritative history source. `log.md` can still be read when present, but we should not create a separate audit log model in this sprint.
- Do not preserve backwards compatibility, legacy inputs, deprecation paths, or versioned tool names. This is a prototype.

## Proposed MCP Tool Contract

Replace OKF and construct-heavy tool names with context-oriented names:

- `list_context_scopes()`
- `list_context_types(scope_id: str | None = None)`
- `list_context_folders(type: str | None = None, scope_id: str | None = None)`
- `read_context_index(folder: str | None = None, scope_id: str | None = None)`
- `read_context_log(folder: str | None = None, scope_id: str | None = None)`
- `list_context_documents(type: str, scope_id: str | None = None, folder: str | None = None, limit: int = 100)`
- `read_context_document(path: str, scope_id: str | None = None)`
- `search_collection(collection: str, query: str, limit: int = 10)`
- `read_collection_source(collection: str, source_id: str)`
- `validate_context()`

Collection tools do not accept `scope_id` or `context_path`. The caller should learn Collection IDs only from scoped folder, index, or Document metadata responses that include `supporting_sources.collections`. MCP should not provide a global Collection listing tool.

## Tool Behavior

### Scope Discovery

- `list_context_scopes()` returns the scope hierarchy from `_scopes.yaml`.
- `list_context_types(scope_id)` returns available Document types visible for the selected scope.
- If no `scope_id` is supplied, discovery remains shallow and metadata-oriented. It should not imply an all-content full-text request.

### Folder And Index Discovery

- `list_context_folders(type, scope_id)` returns folders that contain visible Documents or reserved navigation files. The optional `type` filter narrows the response to folders containing visible Documents of that type.
- `read_context_index(folder, scope_id)` returns `index.md` when present, with headings, links, content hash, and scoped visible entries.
- `read_context_log(folder, scope_id)` returns `log.md` when present and may include Git-derived recent changes for that folder.

### Document Discovery And Read

- `list_context_documents(...)` returns metadata only:
  - `title`
  - `path`
  - `type`
  - `scope_id`
  - `status`
  - `criticality`
  - `description`
  - `supporting_sources.collections`
  - `content_hash`
  - `links`
  - `citations`
- `list_context_documents(...)` must not return `body`.
- `read_context_document(path, scope_id)` returns full Document text only after validating that the Document is visible for the requested scope.

### Collection Search And Source Read

- `search_collection(collection, query, limit)` searches a Collection ID that was surfaced from a scoped Document or folder response.
- The default `limit` is `10`.
- Search returns snippets and current metadata:
  - `collection_id`
  - `source_id`
  - `source_title`
  - logical `source_path`
  - `location`
  - `unit_id`
  - `snippet`
  - `content_hash`
  - retrieval score fields already supported by the Collection manager
- `read_collection_source(collection, source_id)` returns a Collection source by ID after the source has been discovered through `search_collection`.
- Collection source reads should return logical source metadata and text. They should not return absolute paths.

## Tool Test Bench Updates

Tool Test Bench should become the local test surface for the MCP contract.

- Add a dedicated MCP Tools panel.
- Provide a tool selector covering every current agent-facing tool.
- Show input fields appropriate to the selected tool.
- Show the exact request payload sent to the server.
- Show response preview and raw JSON response.
- Show governance and validation errors clearly.
- Use the same server-side service methods as MCP so the bench does not drift from the agent contract.
- Do not present a global Collection browser for MCP testing.
- For Collection tools, populate Collection choices from the selected scoped folder, index, or Document result.

## Context Repository Reorganization

We need to fix competitor scoping so competitive context is retrieved at the correct business or product level.

### Competitor Scope Rules

- Competitor brand pages should remain broad with `scope_id: zoominfo` because one competitor brand can overlap many products.
- Competitor sub-products should map to the matching ZoomInfo product scope when possible using `zi_overlap_product`.
- Competitive crossovers should map to the relevant ZoomInfo product scope.
- Competitive categories should remain broad by default. We should only add category-like scopes if we intentionally introduce category scopes.

### Example

`context_repo/competitors/sub-products/apollo-b2b-data.md` currently uses:

```yaml
zi_overlap_product: Data (Pillar 1)
scope_id: zoominfo
```

It should use:

```yaml
zi_overlap_product: Data (Pillar 1)
scope_id: product-data
```

### Mapping Work

- Build a deterministic mapping from known `zi_overlap_product` values to existing product scopes in `context_repo/_scopes.yaml`.
- Update `context_repo/competitors/sub-products/*.md` where a reliable product match exists.
- Update `context_repo/competitors/crossovers/*.md` where a reliable product match exists.
- Leave competitor brands at `scope_id: zoominfo`.
- Leave competitive categories at `scope_id: zoominfo` unless a specific product scope is clearly warranted.
- Regenerate or update competitor `index.md` files so agents can see product-scoped groupings without opening every file.
- Validate the full context repo after changes.

## Implementation Tasks

### Task 1: MCP Contract Tests

- [x] Add failing tests for the new MCP tool names.
- [x] Add tests proving aggregate Document tools do not return body text.
- [x] Add tests proving full body text is returned only by `read_context_document`.
- [x] Add tests proving no MCP tool exposes semantic search over Documents.
- [x] Add tests proving MCP exposes no global Collection listing tool.

### Task 2: Context Service Retrieval Methods

- [x] Add service methods for scoped folder, type, index, log, and Document metadata retrieval.
- [x] Add service method for scoped Document full-text retrieval.
- [x] Include `supporting_sources.collections` in scoped folder, index, and Document metadata responses.
- [x] Add service methods for governed Collection search and source read.

### Task 3: MCP Tool Rename And Removal

- [x] Add the new context-oriented MCP tools.
- [x] Remove or hide confusing OKF and construct-oriented names from the MCP surface.
- [x] Remove `assemble_context_package`.
- [x] Keep internal OKF terminology where it belongs in implementation modules.
- [x] Ensure MCP caller identity still fails closed unless an explicit service-account role is configured.

### Task 4: Tool Test Bench MCP Panel

- [x] Add a Tool Test Bench panel for all MCP tools.
- [x] Add dynamic input controls for each selected tool.
- [x] Show request payload, response preview, raw JSON, and errors.
- [x] Ensure Collection testing uses Collection IDs surfaced from scoped folder, index, or Document responses.

### Task 5: Competitor Scope Reorganization

- [x] Create tests or scripts that report competitor files whose `zi_overlap_product` can map to an existing product scope but still use `scope_id: zoominfo`.
- [x] Update competitor sub-product scopes using the deterministic mapping.
- [x] Update competitive crossover scopes using the deterministic mapping.
- [x] Keep competitor brand scopes broad.
- [x] Keep competitive category scopes broad unless a product match is explicit.
- [x] Update competitor indexes to support scoped progressive disclosure.

### Task 6: Verification

- [x] Run `uv run pytest`.
- [x] Run `uv run python run.py validate`.
- [x] Run `npm run build` for the CMS.
- [x] Run Tool Test Bench demos for representative scope, Document, and Collection flows.

## Acceptance Criteria

- MCP exposes context-oriented tool names that match the governed retrieval model.
- Aggregate Document discovery returns metadata only and never returns full body text.
- Full Document body text is available only through explicit Document read.
- Collection semantic search uses Collection IDs surfaced from scoped folder, index, or Document metadata.
- Collection source reads are available only for sources discovered through Collection search.
- `assemble_context_package` is removed from the MCP surface.
- Tool Test Bench can test every MCP tool from the browser.
- Tool Test Bench shows payloads, responses, raw JSON, and governance errors.
- Competitor sub-products and crossovers are scoped to matching product scopes where reliable mappings exist.
- Competitor brand pages remain broad.
- Competitive categories remain broad unless intentionally changed.
- Validation passes with no invalid OKF Documents.

## Non-Goals

- Do not add `tags` to the MCP discovery contract.
- Do not add semantic search over Documents.
- Do not add `scope_mode`.
- Do not add category scopes unless we explicitly decide to model categories as scopes.
- Do not add Collection summarization.
- Do not auto-promote Collection evidence into Documents.
- Do not add a new role taxonomy.
- Do not create a separate audit log system beyond Git history and existing records.
- Do not keep compatibility code for old MCP tool names or request shapes.
