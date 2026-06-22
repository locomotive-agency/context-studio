# Next Sprint: Access Control And Production Hardening

## Goal

Make authentication, authorization, and deployment safety match the product model already described in the archived sprint docs and `GOVERNANCE.md`.

This sprint is not about adding new governance concepts. It is about moving existing policy to the right boundaries, removing hard-coded demo assumptions from source files, and making API and MCP access behave the same way.

## Sources Reviewed

- `GOVERNANCE.md`
- `archive/2026-06-21-next-sprint-user-permissions.md`
- `archive/2026-06-21-plan-prototype-architecture.md`
- `archive/2026-06-21-curated-context-plus-searchable-collections.md`
- Current implementation in `context_system/app.py`, `context_system/auth.py`, `context_system/config.py`, `context_system/mcp_server.py`, `context_system/service.py`, and `cms/src/pages/index.astro`

## Role Model

Keep the role model simple.

- Admins can edit everything, including users, scopes, schemas, folders, documents, Collections, imports, history restore, and system-level settings exposed in the app.
- Editors can edit document folders and documents, and can add or manage Collections and Collection source files.
- Viewers can review context and request context through the app, API, and MCP tools. Viewers cannot write content or configuration.

Do not introduce per-record authorization. The three role abilities above are the permission model, so `edit_roles` metadata should be removed from schemas, models, UI, and runtime records instead of being preserved as a parallel hint.

## Priority 0: Move Demo Defaults Into Config And Fail Closed

### Problem

Default users are currently created directly in `context_system/auth.py`, and the session signing key defaults to `change-me-in-production` in `context_system/config.py`. This makes local demo behavior too easy to carry into hosted mode.

### What Changes

Backend:

- Move local demo users out of `UserStore.__init__` and into `Config`.
- Add explicit config for local demo auth, such as:
  - `auth_mode`: `local_demo` or `github`
  - `local_demo_users`: the seed users for local development
  - `allow_local_demo_users`: defaults to `true` only for local development
- Keep the sample demo users in configuration, not as hidden source-file behavior.
- Fail startup when production-looking settings use unsafe defaults:
  - `CS_SECRET_KEY` is missing or still equals `change-me-in-production`
  - local demo auth is enabled with a non-local `CS_PUBLIC_APP_URL`
  - GitHub auth is partially configured
- Keep local setup easy, but make production intent explicit.

Tests:

- Add config tests proving demo users are seeded from `Config`.
- Add startup/config tests proving unsafe production combinations fail fast.
- Add a local demo test proving `admin/admin123`, `editor/editor123`, and `viewer/viewer123` still work when explicitly enabled.

Docs:

- Update `README.md` so demo credentials are clearly local-only.
- Document the required production environment variables and the failure behavior.

### Files Likely To Change

- `context_system/config.py`
- `context_system/auth.py`
- `context_system/app.py`
- `tests/test_context_service.py`
- `tests/test_role_access.py`
- new `tests/test_config_safety.py`
- `README.md`

## Priority 1: Use One Authorization Boundary For API And MCP

### Problem

The API route layer receives a user, but MCP tools call the service without carrying user identity into the tool functions. GitHub permission refresh also happens on write paths, but read and MCP data access can rely on cached session role.

### What Changes

Backend:

- Add small, explicit helpers for role checks:
  - `require_viewer(user)`
  - `require_editor(user)`
  - `require_admin(user)`
- Use those helpers consistently in API routes.
- Make GitHub-backed access refresh or revalidate before data leaves the system, not only before writes.
- Pass authenticated user context into MCP tool execution.
- Remove service behavior that treats missing user context as admin.
- Make `assemble_context_package_v1` require a user when it needs to filter MCP supporting sources.
- Keep the service as the decision point for governed lookup, package assembly, supporting-source filtering, and audit behavior.

Tests:

- Add tests proving API context routes reject missing login.
- Add tests proving MCP context tools reject missing login.
- Add tests proving MCP supporting-source RBAC uses the signed-in user's role.
- Add tests proving a GitHub user whose repository permission has been removed cannot keep reading context after permission refresh.

### Files Likely To Change

- `context_system/auth.py`
- `context_system/app.py`
- `context_system/mcp_server.py`
- `context_system/service.py`
- `tests/test_role_access.py`
- new `tests/test_mcp_auth.py`

## Priority 2: Align Route Permissions With The Product Role Model

### Problem

Some current routes and UI controls are close to the intended model, but the boundary should be made explicit and tested. Admin-only configuration work should not blur into Editor content work.

### What Changes

Backend route policy:

- Admin-only:
  - user management
  - scopes
  - schemas and folder metadata defaults
  - OKF folder import
  - system-level configuration surfaces, if any are added later
- Editor or Admin:
  - create, edit, delete, and restore documents
  - create and delete document folders
  - create Collections
  - upload or index Collection source files
- Viewer, Editor, or Admin:
  - list and read documents
  - list records
  - run validation reports
  - inspect history and diffs
  - list Collections and Collection documents
  - request context packages
  - use MCP context tools

Frontend:

- Show Admin controls only to Admins.
- Show document, folder, and Collection editing controls to Editors and Admins.
- Keep Viewer surfaces focused on review, validation, history, and context requests.
- Remove `edit_roles` from document and folder metadata controls.
- Do not rely on hidden UI controls as the only enforcement. API and MCP checks remain authoritative.

Tests:

- Admin can edit users, schemas, scopes, folders, documents, and Collections.
- Editor can edit folders, documents, and Collections.
- Editor cannot edit users, schemas, or scopes.
- Viewer can review and request context.
- Viewer cannot write users, schemas, scopes, folders, documents, Collections, or imports.
- Runtime records and API responses no longer expose `edit_roles`.

### Files Likely To Change

- `context_system/app.py`
- `context_system/models.py`
- `context_system/repository.py`
- `context_repo/_schema.yaml`
- `cms/src/pages/index.astro`
- `tests/test_role_access.py`
- `README.md`

## Priority 3: Fence Local-Only Filesystem Workflows

### Problem

OKF folder import accepts a server-visible folder path. That is useful locally, but it is too broad for hosted mode unless explicitly fenced.

### What Changes

Backend:

- Add config for whether server-path OKF imports are enabled.
- Default server-path imports to local demo mode only.
- In hosted mode, reject arbitrary `source_folder` imports unless a controlled staging directory is configured.
- Resolve import paths and reject paths outside the allowed import root.
- Reject symlinks during import scan and apply.
- Keep the one-commit import behavior.

Tests:

- Local demo mode can import from an allowed local folder.
- Hosted mode rejects arbitrary server paths.
- Imports outside the configured import root are rejected.
- Symlinks are rejected.

### Files Likely To Change

- `context_system/config.py`
- `context_system/importer.py`
- `context_system/service.py`
- `context_system/app.py`
- `tests/test_next_sprint.py`
- new `tests/test_import_security.py`

## Priority 4: Add Basic Collection Upload Guardrails

### Problem

Collections are the right boundary for supporting sources, but upload and parsing behavior needs production guardrails before hosting.

### What Changes

Backend:

- Add configurable maximum upload size.
- Add configurable allowed source file extensions or MIME types.
- Avoid returning absolute server paths in public citations. Return logical paths or source document IDs.
- Store parser errors without leaking server-local filesystem details.
- Keep the product rule from the archived sprint: Collections do not get scope, criticality, context type, allowed-use settings, summarization, or automatic OKF promotion.

Tests:

- Oversized uploads are rejected.
- Disallowed file types are rejected.
- Collection citations do not expose absolute server paths.
- Parser errors do not expose local server paths.
- Existing Collection routing through OKF `supporting_sources.collections` still works.

### Files Likely To Change

- `context_system/config.py`
- `context_system/collections.py`
- `context_system/service.py`
- `tests/test_next_sprint.py`
- new `tests/test_collection_security.py`

## Acceptance Criteria

- Demo users are seeded from `Config`, not hard-coded in `auth.py`.
- Production-looking startup fails when the secret key or auth mode is unsafe.
- Admins can edit everything, including users, schemas, scopes, folders, documents, and Collections.
- Editors can edit document folders and documents, and can add or manage Collections.
- Viewers can review and request context through API and MCP, but cannot write.
- `edit_roles` is removed from the schema, UI, runtime records, and API responses.
- API and MCP use the same authentication and role model.
- GitHub permission revocation is respected before context data leaves the system.
- Arbitrary server-folder import is local-only or constrained to an explicit import root.
- Collection upload and parsing have basic size, type, citation, and error-leakage guardrails.
- Tests directly cover Admin, Editor, Viewer, missing-login, GitHub refresh, MCP access, import safety, and Collection upload safety.
- `README.md` describes only this permission model and makes local demo behavior explicit.

## Non-Goals

- Do not add a new role taxonomy.
- Do not add Collection summarization.
- Do not search OKF records semantically.
- Do not split the prototype into multiple deployments.
