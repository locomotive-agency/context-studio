# OKF And MCP Agent Retrieval Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Follow the checkbox order and update this file as each task is completed.

**Goal:** Make MCP the governed agent-facing retrieval surface for OKF records and OKF-routed Collection evidence.

**Architecture:** OKF folder and file schema remains the governance source of truth. MCP clients request context by OKF type and optional scope/query; the service resolves effective schema, approved OKF records, and any allowed Collection evidence. Collections are never exposed through MCP as a standalone browse or arbitrary search surface.

**Tech Stack:** FastAPI, FastMCP, Pydantic, SQLite FTS5 Collections, Git-backed OKF repository, Astro CMS, pytest.

---

## Sources Reviewed

- `GOVERNANCE.md`
- Karpathy LLM Wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Google OKF spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- Marketing context spec: `C:/Users/jroak/Downloads/structuring-marketing-context-for-ai-improved.md`
- Current implementation in `context_system/app.py`, `context_system/mcp_server.py`, `context_system/service.py`, `context_system/repository.py`, `context_system/cms.py`, `context_system/okf.py`, `context_system/models.py`, and `context_system/collections.py`

## Review Clarifications

- The earlier "canonical label or alias resolver" item is removed. It was a solution looking for a problem. For now, skills and MCP callers should use the OKF `type` values defined in folder and file schema.
- Supplying user context to MCP is not meant to personalize the AI session. Its value is authorization and auditability: MCP should not become a way to bypass Admin, Editor, and Viewer permissions. If a deployment intentionally runs MCP as one local trusted user, that should be represented as an explicit configured service account role, not as missing identity defaulting to Admin.
- Collections must be reached only through OKF governance. MCP should not list Collections, list Collection documents, or accept arbitrary Collection IDs for search. The service may search Collection evidence only after resolving the OKF folder/file schema for the requested context type and scope.
- Avoid `v1`, `v2`, `v3` function names unless there is a concrete compatibility need. Use one current context-package contract and keep versioning at the API/schema boundary only if a real migration requires it.
- Required MCP request fields should either affect retrieval or be required for traceability. Do not require fields that the service ignores.
- Do not add server-generated run workflows or a broader audit subsystem in this sprint. Keep existing explicit `run_id` audit behavior unless a concrete audit workflow is defined.

## Current Request Contract

The current MCP `assemble_context_package` tool accepts more fields than the service meaningfully uses.

- `task`: required by the tool. It is echoed in the response and can be used for audit context, but it does not change which OKF records or Collection evidence are selected.
- `requests`: optional in the current tool because of a legacy `constructs` path. The new contract should make `requests` required and non-empty.
- `requests[].type`: required in each request item. This changes the response because it selects the OKF records, effective schema, criticality, and Collection routing.
- `requests[].query`: optional. This changes the response only when the resolved schema allows Collection evidence and the service searches those routed Collections.
- `scope_id`: optional. This changes the response because it controls scoped record and schema resolution.
- `run_id`: optional. This affects audit records only. It should not be required to retrieve context.
- `constructs` and `icp`: legacy inputs. Remove them from the MCP contract if they do not affect the current retrieval path.

## Alignment Summary

The repository is directionally aligned with the desired architecture:

- OKF documents are stored as markdown with YAML frontmatter.
- Unknown OKF frontmatter keys are tolerated.
- Collections are separate supporting evidence buckets instead of governed context records.
- Context package assembly already routes Collection search through OKF `supporting_sources.collections`.
- API calls pass the authenticated user into context package assembly.
- Admin, Editor, and Viewer roles are the active permission model.

The remaining gaps are:

- MCP authenticates the HTTP request but does not pass caller identity or an explicit service-account role into tool execution.
- Missing user context currently risks Admin-like behavior in MCP supporting-source filtering.
- MCP tools require callers to already know a context `type`; they do not expose OKF bundle discovery, folder traversal, indexes, logs, types, scopes, links, or citations.
- `index.md` and `log.md` are preserved as reserved OKF files but hidden from normal document listing and not exposed as first-class navigation/history resources.
- MCP does not yet expose a governed way to request Collection evidence through OKF folder/file schema.
- Context package responses are raw dicts instead of a validated response model at the API and MCP boundary.
- OKF links and `# Citations` sections are not parsed into structured fields for agents.

## Role And Security Rules

- Admins can edit everything, including users, scopes, schemas, folders, documents, Collections, imports, history restore, and system settings.
- Editors can edit document folders and documents, and can add or manage Collections and Collection source files.
- Viewers can review context and request context through the app, API, and MCP tools.
- Do not add per-record edit metadata. `edit_roles` is not part of the model.
- Add RBAC checks anywhere data leaves the system or an external tool can be invoked.
- Missing MCP caller identity must fail closed unless an explicit service-account role is configured.
- Missing MCP caller identity must never imply Admin.

## Priority 0: Fail Closed On MCP Authorization Context

### Problem

`context_system/app.py` checks login for `/mcp`, but `context_system/mcp_server.py` invokes `ContextService` without a user. `ContextService._rbac_mcp_sources()` currently treats missing user context as Admin.

This does not add user-visible value to an AI session by itself. It matters because MCP returns governed data and may suggest external MCP sources. If identity is dropped at the tool layer, MCP can become a permission bypass.

### Required Changes

- Add a small request context module, for example `context_system/request_context.py`, backed by `contextvars.ContextVar`.
- In the `/mcp` middleware in `context_system/app.py`, resolve `current_user(request)`, store the public user in the context var before `call_next`, and reset it afterward.
- In MCP tools that return data or source suggestions, read the current user from the context var and pass it into service methods.
- If the project needs a local single-user MCP mode, add explicit config such as `mcp_service_account_role: viewer|editor|admin` and require it to be set. Do not infer Admin from a missing user.
- Remove the Admin fallback in `ContextService._rbac_mcp_sources()`.
- Missing MCP user context should deny configured MCP source access and report `missing authenticated user` unless an explicit service-account role is configured.

### Tests

- Add `tests/test_mcp_auth.py`.
- Prove unauthenticated MCP calls are rejected when no service-account role is configured.
- Prove an MCP context package assembled as Viewer does not receive Admin-only MCP supporting sources.
- Prove missing user context does not default to Admin in `ContextService._rbac_mcp_sources()`.
- Prove API `/api/context-package` and MCP `assemble_context_package` apply the same source filtering for the same user role.
- Prove explicit local service-account mode uses the configured role and nothing broader.

## Priority 1: Add Agent-Oriented OKF Discovery And Traversal Tools

### Problem

The OKF spec expects lightweight markdown files, links, `index.md`, and `log.md` to support progressive disclosure. The Karpathy LLM wiki pattern depends on an agent being able to inspect a maintained wiki, its index, its log, and its schema.

Current MCP tools expose `get_construct`, deprecated `search_context`, `assemble_context_package`, and validation. An agent cannot start from MCP and ask what OKF bundle exists, which folders exist, which concepts are available, or what `index.md` says.

### Required Changes

- Add content-store methods that can include reserved OKF files:
  - `list_okf_entries(folder: str | None = None)`
  - `read_okf_entry(path: str)`
  - `read_okf_index(folder: str | None = None)`
  - `read_okf_log(folder: str | None = None)`
- Treat `index.md` and `log.md` as valid OKF navigation documents even though they do not require YAML frontmatter.
- Keep `ContentStore.list_documents()` focused on editable concept documents if that is still useful for the CMS, but add explicit OKF traversal methods for agents.
- Add MCP tools:
  - `list_okf_bundle(folder: str | None = None)`
  - `read_okf_document(path: str)`
  - `read_okf_index(folder: str | None = None)`
  - `read_okf_log(folder: str | None = None)`
  - `list_okf_types(scope_id: str | None = None)`
  - `list_okf_scopes()`
- Return stable fields for each entry: `path`, `kind`, `title`, `type`, `scope_id`, `status`, `description`, `links`, `citations`, `content_hash`, and validation status when applicable.
- Keep unknown OKF types and unknown frontmatter keys tolerant.

### Tests

- Add tests proving `index.md` and `log.md` can be read through OKF traversal without frontmatter.
- Add tests proving concept documents still require a non-empty `type`.
- Add tests proving MCP `list_okf_bundle` exposes folders, concept docs, `index.md`, and `log.md`.
- Add tests proving unknown OKF frontmatter keys are preserved in agent-facing responses.

## Priority 2: Keep Collection Evidence Routed Through OKF Schema

### Problem

Collections are supporting evidence, not independent governed context. They should be pointed to by document folder and file schema, then searched only as part of a governed context request.

The previous plan overexposed Collections by proposing MCP tools that could list and search Collections directly. That is not aligned with the governance model.

### Required Changes

- Do not add MCP tools named `list_collections`, `list_collection_documents`, `search_collection`, or any tool that accepts an arbitrary `collection_id` from an MCP client.
- Add or keep only a context-package path where the MCP caller requests OKF context:
  - `task`
  - `scope_id`
  - `requests[].type`
  - `requests[].query`
- Resolve Collection access inside `ContextService` by using `ContextRepository.supporting_sources_for(type, scope_id)`.
- `supporting_sources_for()` must merge Collection IDs only from effective folder schema and file frontmatter.
- Search only the resolved `supporting_sources.collections` values for the requested OKF type and scope.
- If no Collection source is routed by the effective OKF schema, return no Collection results.
- If a query is omitted, return approved OKF records and source metadata, but do not run Collection search.
- Return Collection evidence inside the context package with citation fields only: `collection_id`, `source_document_id`, `source_title`, logical `source_path`, `location`, `unit_id`, and `content_hash`.
- Do not expose absolute server paths in MCP results.
- Do not promote Collection excerpts into OKF records automatically.
- Do not add Collection scope, criticality, status, allowed-use, or summarization fields.

### Tests

- Prove MCP has no direct Collection listing or arbitrary Collection search tool.
- Prove an MCP caller cannot pass `collection_id` to search a Collection directly.
- Prove Collection search occurs only for Collections routed by effective OKF folder or file schema.
- Prove a request for the same `type` and `query` returns different Collection evidence when `scope_id` changes the effective schema.
- Prove a request with no routed Collections returns no Collection evidence.
- Prove Collection results include citations and no absolute server filesystem paths.

## Priority 3: Use One Typed Context Package Boundary

### Problem

`ContextPackageV1Request` is typed, but `assemble_context_package_v1()` returns a raw dict. `ContextPackageV1Result` exists but is only a result item model, not the full response envelope.

The typing gap is real, but the `v1` naming creates avoidable complexity. We do not need `v1`, `v2`, and `v3` service functions unless there is a real compatibility migration.

### Required Changes

- Rename current models and methods toward one current contract:
  - `ContextPackageRequest`
  - `ContextPackageResponse`
  - `ContextPackageResult`
  - `ContextService.assemble_context_package(...)`
- Keep one implementation path for `/api/context-package` and MCP `assemble_context_package`.
- Deprecate or remove legacy inputs that do not affect retrieval, especially `constructs` and `icp`.
- Add a Pydantic response envelope with:
  - `task`
  - `scope_id`
  - `results`
  - `blocked`
  - `kb_git_sha`
  - `run_id`, only when supplied by the caller
- Build and validate the response model before returning `model_dump()`.
- Include structured OKF provenance for each OKF record: `kb_path`, `content_hash`, `okf` frontmatter, `links`, and `citations`.
- Preserve `missing` blocks and `access_issues` in the typed response.

### Tests

- Add response-shape tests for API and MCP context package assembly.
- Prove invalid service output cannot leave the boundary without validation.
- Prove controlled missing context still sets `blocked: true`.
- Prove Collection citations validate against the response model.
- Prove `constructs` and `icp` are not required by the MCP contract.

## Priority 4: Parse OKF Links, Citations, Indexes, And Logs

### Problem

The OKF spec keeps links and citations lightweight, and the Karpathy wiki pattern depends on curated navigation and history. The current implementation returns markdown bodies but does not expose links, citations, indexes, or logs as structured agent-readable fields.

### Required Changes

- Add a small markdown metadata parser in `context_system/okf.py` or a focused new module.
- Extract:
  - internal markdown links to other OKF files
  - external links
  - `# Citations` section entries
  - headings for quick outline previews
- Attach parsed fields to runtime records and OKF traversal responses.
- For `index.md`, return a folder-level navigation response with body, links, headings, and content hash.
- For `log.md`, return chronological entries if they can be parsed safely; otherwise return body, headings, links, and content hash.
- Keep parsing tolerant. Broken links should be surfaced as validation warnings, not fatal errors.

### Tests

- Prove citations under `# Citations` are extracted.
- Prove broken markdown links are reported but do not prevent document retrieval.
- Prove internal links are returned with normalized repository-relative paths.
- Prove `index.md` and `log.md` return content hashes.

## Acceptance Criteria

- MCP uses either the authenticated user role or an explicit configured service-account role.
- Missing MCP user identity fails closed unless an explicit service-account role is configured.
- Missing MCP user identity never defaults to Admin.
- AI systems can use MCP to list OKF folders, read `index.md`, read `log.md`, list OKF types and scopes, retrieve OKF concepts, inspect links, and inspect citations.
- AI systems request Collection evidence only through context package requests governed by OKF folder/file schema.
- MCP does not expose direct Collection listing, direct Collection document listing, arbitrary Collection IDs, or arbitrary Collection search.
- Collection evidence is returned with citations and logical paths, not absolute server paths.
- Context packages are validated by typed response models before leaving the service.
- Required MCP request fields are limited to fields that affect retrieval or traceability.
- The role model remains Admin, Editor, Viewer.
- `edit_roles` is not reintroduced.

## Non-Goals

- Do not add semantic search over OKF records as the primary retrieval path.
- Do not add Collection summarization.
- Do not auto-promote Collection evidence into OKF.
- Do not expose Collections as a standalone MCP browsing or search surface.
- Do not accept arbitrary Collection IDs in MCP context requests.
- Do not add a central OKF schema registry.
- Do not add per-record edit permissions.
- Do not add a canonical label or alias resolver in this sprint.
- Do not add server-generated run IDs or a broader audit workflow in this sprint.
- Do not add a new role taxonomy.
