# OKF And MCP Agent Retrieval Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Follow the checkbox order and update this file as each task is completed.

## Goal

Make MCP the canonical agent-facing retrieval surface for OKF records and Collection evidence.

AI systems should be able to use MCP to discover what context exists, traverse OKF `index.md` and `log.md`, retrieve approved OKF concepts, search only the Collections routed by governed metadata, receive citations and content hashes, and respect the same role policy as the API and UI.

## Sources Reviewed

- `GOVERNANCE.md`
- Karpathy LLM Wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Google OKF spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- Marketing context spec: `C:/Users/jroak/Downloads/structuring-marketing-context-for-ai-improved.md`
- Current implementation in `context_system/app.py`, `context_system/mcp_server.py`, `context_system/service.py`, `context_system/repository.py`, `context_system/cms.py`, `context_system/okf.py`, `context_system/models.py`, and `context_system/collections.py`

## Alignment Summary

The repository is directionally aligned with the desired architecture:

- OKF documents are stored as markdown with YAML frontmatter.
- Unknown OKF frontmatter keys are tolerated.
- Collections are separate supporting evidence buckets instead of governed context records.
- Context package assembly already routes Collection search through OKF `supporting_sources.collections`.
- API calls pass the authenticated user into context package assembly.
- Admin, Editor, and Viewer roles are the active permission model.

The gaps are mostly in the agent-facing surface:

- MCP authenticates the HTTP request but does not pass caller identity into tool execution.
- MCP tools require callers to already know a context `type`; they do not expose OKF bundle discovery, folder traversal, indexes, logs, types, scopes, links, or citations.
- `index.md` and `log.md` are preserved as reserved OKF files but hidden from normal document listing and not exposed as first-class navigation/history resources.
- Collections can be listed through HTTP API routes, but MCP does not expose Collection discovery or governed Collection evidence search.
- Context package v1 returns an untyped dict instead of a validated response model at the API and MCP boundary.
- There is no canonical label or alias resolver between skill prompts and OKF record types.
- OKF links and `# Citations` sections are not parsed into structured fields for agents.
- Controlled context audit is skipped unless callers provide a `run_id`.

## Role And Security Rules

- Admins can edit everything, including users, scopes, schemas, folders, documents, Collections, imports, history restore, and system settings.
- Editors can edit document folders and documents, and can add or manage Collections and Collection source files.
- Viewers can review context and request context through the app, API, and MCP tools.
- Do not add per-record edit metadata. `edit_roles` is not part of the model.
- Add RBAC checks anywhere data leaves the system or an external tool can be invoked.
- Missing MCP caller identity must fail closed. It must never imply Admin.

## Priority 0: Carry Authenticated User Context Into MCP Tools

### Problem

`context_system/app.py` checks login for `/mcp`, but `context_system/mcp_server.py` invokes `ContextService` without a user. `ContextService._rbac_mcp_sources()` currently treats missing user context as Admin.

That is not aligned with `GOVERNANCE.md` because data leaves the system through MCP. It also prevents MCP packages from enforcing source policy for Viewers, Editors, and Admins.

### Required Changes

- Add a small request context module, for example `context_system/request_context.py`, backed by `contextvars.ContextVar`.
- In the `/mcp` middleware in `context_system/app.py`, resolve `current_user(request)`, store the public user in the context var before `call_next`, and reset it afterward.
- In every MCP tool in `context_system/mcp_server.py`, read the current user from the context var and pass it into service methods that return data or suggest external sources.
- Make MCP tools fail with a clear authorization error when no authenticated MCP user is available.
- Remove the Admin fallback in `ContextService._rbac_mcp_sources()`. Missing user context should deny configured MCP source access and report `missing authenticated user`.
- Decide whether the standalone `python -m context_system.mcp_server` path is local-demo-only. If retained, require an explicit config flag for unauthenticated local use.

### Tests

- Add `tests/test_mcp_auth.py`.
- Prove unauthenticated MCP calls are rejected.
- Prove an MCP context package assembled as Viewer does not receive Admin-only MCP supporting sources.
- Prove missing user context does not default to Admin in `ContextService._rbac_mcp_sources()`.
- Prove API `/api/context-package` and MCP `assemble_context_package` apply the same source filtering for the same user role.

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

## Priority 2: Expose Governed Collection Evidence Through MCP

### Problem

Collections are part of the desired evidence model, but MCP clients cannot discover Collections or search governed Collection sources directly. The only Collection search path is inside `assemble_context_package_v1`, and only when the caller already knows the exact context type and query.

AI systems need MCP tools that make Collection evidence findable while preserving the rule that OKF records are governed context and Collections are supporting evidence.

### Required Changes

- Add MCP tools:
  - `list_collections()`
  - `list_collection_documents(collection_id: str)`
  - `list_supporting_sources(type: str, scope_id: str | None = None)`
  - `search_supporting_collections(type: str, query: str, scope_id: str | None = None, top_k: int = 5)`
- Route `search_supporting_collections` through `ContextRepository.supporting_sources_for()` so agents can search only the Collections attached to the requested OKF type and scope.
- Return Collection results with citation fields only: `collection_id`, `source_document_id`, `source_title`, logical `source_path`, `location`, `unit_id`, and `content_hash`.
- Do not expose absolute server paths in MCP results.
- Do not promote Collection excerpts into OKF records automatically.
- Do not add Collection scope, criticality, status, allowed-use, or summarization fields.

### Tests

- Prove Viewers, Editors, and Admins can list Collections through MCP.
- Prove unauthenticated MCP callers cannot list or search Collections.
- Prove `search_supporting_collections` searches only Collections routed by OKF `supporting_sources.collections`.
- Prove Collection results include citations and no absolute server filesystem paths.

## Priority 3: Make Context Package V1 A Typed Boundary

### Problem

`ContextPackageV1Request` is typed, but `assemble_context_package_v1()` returns a raw dict. `ContextPackageV1Result` exists but is only a result item model, not the full response envelope.

That is not aligned with the governance rule to use typed request and response models at API boundaries.

### Required Changes

- Add a Pydantic response envelope model, for example `ContextPackageV1Response`, with:
  - `task`
  - `scope_id`
  - `results`
  - `blocked`
  - `kb_git_sha`
  - `run_id`
  - `audit_id` or `audit_written`
- Change `ContextService.assemble_context_package_v1()` to build and validate the response model before returning `model_dump()`.
- Reuse the same response model for `/api/context-package`, `/api/assemble_context_package`, and MCP `assemble_context_package`.
- Include structured OKF provenance for each OKF record: `kb_path`, `content_hash`, `okf` frontmatter, `links`, and `citations`.
- Preserve `missing` blocks and `access_issues` in the typed response.

### Tests

- Add response-shape tests for API and MCP context package assembly.
- Prove invalid service output cannot leave the boundary without validation.
- Prove controlled missing context still sets `blocked: true`.
- Prove Collection citations validate against the response model.

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

## Priority 5: Add Canonical Label And Alias Resolution

### Problem

Skills and prompts should be able to request context by stable labels. The service currently looks up exact OKF `type` values only. That makes agents brittle and forces prompts to know repository internals.

### Required Changes

- Add a canonical label resolver in the service layer.
- Store aliases in one governed place, such as `_context_aliases.yaml` or a config-backed registry.
- Resolve aliases before:
  - `get_construct`
  - `assemble_context_package_v1`
  - `list_supporting_sources`
  - `search_supporting_collections`
- Return the requested label and resolved OKF type in package results.
- Make ambiguous aliases a clear validation error.
- Do not use aliases for authorization. Roles remain Admin, Editor, and Viewer.
- Do not reintroduce `edit_roles`.

### Tests

- Prove an alias resolves to a canonical OKF type.
- Prove an ambiguous alias fails with a clear error.
- Prove aliases work the same over API and MCP.
- Prove authorization is still based only on the signed-in user role.

## Priority 6: Make Controlled Usage Audit Reliable

### Problem

Controlled context usage is only audited when a caller provides `run_id`. Agents may forget to send one, especially over MCP.

### Required Changes

- Generate a server-side `run_id` when controlled context is used and the caller did not provide one.
- Include `run_id` in the context package response.
- Write audit records whenever controlled OKF records are included in API or MCP context packages.
- Include record IDs, content hashes, `kb_git_sha`, task, timestamp, and caller identity.
- Do not audit raw Collection excerpts unless they are included as supporting evidence in the returned package; when audited, store citation identifiers and hashes, not full extracted text.

### Tests

- Prove controlled package assembly writes an audit record without caller-provided `run_id`.
- Prove package response includes generated `run_id`.
- Prove audit entries include caller identity and OKF content hashes.
- Prove flexible-only packages do not write controlled-use audit records.

## Acceptance Criteria

- MCP uses the same authenticated user and role model as the API.
- Missing MCP user identity fails closed.
- Missing user context never defaults to Admin.
- AI systems can use MCP to list OKF folders, read `index.md`, read `log.md`, list OKF types and scopes, retrieve OKF concepts, inspect links, and inspect citations.
- AI systems can use MCP to list Collections, list Collection documents, and search governed supporting Collections by OKF type or alias.
- Collection evidence is returned with citations and logical paths, not absolute server paths.
- Context packages are validated by typed response models before leaving the service.
- Controlled context usage is audited even when MCP clients omit `run_id`.
- Alias resolution lets skills use stable labels without embedding repository internals.
- Unknown OKF fields, unknown OKF types, and broken links remain tolerant according to OKF conformance.
- The role model remains Admin, Editor, Viewer.
- `edit_roles` is not reintroduced.

## Non-Goals

- Do not add semantic search over OKF records as the primary retrieval path.
- Do not add Collection summarization.
- Do not auto-promote Collection evidence into OKF.
- Do not add a central OKF schema registry.
- Do not add per-record edit permissions.
- Do not add a new role taxonomy.
