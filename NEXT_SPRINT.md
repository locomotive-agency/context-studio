# Next Sprint: User Permissions

## Goal

Make the app, API, and MCP server follow the same simple permission model.

All access requires login:

- local development uses username and password
- production uses GitHub login

Logged-in users have one of three roles:

- Admins can edit users and everything else.
- Editors can edit Folders, Documents, and Collections.
- Viewers can request context and semantic data.

## Work

### Backend Permissions

Make API and MCP data access require a valid logged-in user.

Route behavior:

- Admin routes allow Admins.
- Editor routes allow Editors and Admins.
- Viewer routes allow Viewers, Editors, and Admins.

Apply that behavior consistently:

- user management routes are Admin routes
- Folder write routes are Editor routes
- Document write routes are Editor routes
- Collection write routes are Editor routes
- context package and retrieval routes are Viewer routes
- MCP context tools are Viewer routes

Every route that returns context or semantic data should use the same login requirement.

### CMS Permissions

Make visible controls match the same roles:

- Admins can use user management and all editing controls.
- Editors can use Folder, Document, and Collection editing controls.
- Viewers can use context request and semantic retrieval surfaces.

### Tests And Docs

Add tests that prove the role behavior directly.

Test coverage:

- local username/password login respects Admin, Editor, and Viewer roles
- GitHub login maps to the same roles in production mode
- requests without a valid login cannot access data
- Admins can edit users and everything else
- Editors can edit Folders, Documents, and Collections
- Editors cannot edit users
- Viewers can request context and semantic data
- Viewers cannot edit Folders, Documents, Collections, or users
- API and MCP context access follow the same login requirement

Update docs:

- `README.md`
- `PLAN.md`

## Acceptance Criteria

- Admins can edit users and everything else.
- Editors can edit Folders, Documents, and Collections.
- Viewers can request context and semantic data.
- App, API, and MCP access require a valid local or GitHub login.
- Route permissions match the three roles above.
- CMS controls match the same permissions as the API.
- Tests cover Admin, Editor, Viewer, and missing-login behavior.
- Docs describe only this permission model.

## Files Likely To Change

Backend:

- `context_system/auth.py`
- `context_system/app.py`
- `context_system/mcp_server.py`

Frontend:

- `cms/src/pages/index.astro`
- `cms/src/styles/global.css`

Tests:

- `tests/test_context_service.py`
- new `tests/test_role_access.py`
- new `tests/test_mcp_auth.py`

Docs:

- `README.md`
- `PLAN.md`

## Sources Reviewed

- `GOVERNANCE.md`
- `PLAN.md`
- Current implementation in `context_system/app.py`, `context_system/auth.py`, `context_system/mcp_server.py`, `cms/`, and `tests/`
