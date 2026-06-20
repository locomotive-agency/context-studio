# Context Documentation System Prototype

This prototype is a file-based context CMS for OKF context documents. Astro provides the CMS interface. FastAPI and Pydantic handle authentication, filesystem operations, OKF validation, scoped retrieval, Git history, and MCP access. FastMCP exposes valid context to AI tools.

## What It Does

- Stores Markdown OKF records and JSON source files in `context_repo/`
- Uses local Git for commits, history, diffs, restores, and deletes
- Supports folder-level metadata inherited by documents
- Lets document frontmatter override folder metadata
- Validates documents for OKF and governance rules
- Provides Raw, Preview, and Split document views
- Exposes MCP tools at `/mcp/`
- Supports local demo users or GitHub-backed access control

## Storage

The project is one Git repository. CMS writes commit only the changed paths under `context_repo/`. In local mode, commits stay local. In GitHub mode, we sync from `origin` on startup, pull with `--ff-only` before a write, commit the changed path, and push back to the current branch.

Governance resolves in this order:

1. `context_repo/_schema.yaml`
2. Each nested folder's `_schema.yaml`
3. The document's YAML frontmatter

Later values override earlier values. Every concept document must still contain its own OKF `type` field.

`context_repo/_scopes.yaml` stores the parent-linked scope hierarchy. Documents use a `scope_id`; context retrieval inherits from parent scopes and prefers the most specific matching records.

CMS creation and editing actions use right-side drawers. Documents can be added, edited, deleted, restored, and reviewed through Git history. Folders can be added and deleted when empty. In local mode, administrators can add, edit, and remove users and scopes. The active user and final administrator account cannot be removed. In GitHub mode, user access is managed in GitHub repository settings.

Markdown files are validated as OKF records. JSON files are supported as structured source documents. Both formats provide Raw, Preview, and Split editor modes. Representative case study, competitive, and ICP examples live under `context_repo/examples/`.

## Run Locally

Terminal 1:

```bash
uv sync
uv run python run.py serve --port 8001
```

Terminal 2:

```bash
cd cms
npm install
npm run dev
```

Open `http://127.0.0.1:4321`.

Default local users are used when GitHub mode is not configured:

- `admin` / `admin123`
- `editor` / `editor123`
- `viewer` / `viewer123`

## GitHub access mode

GitHub can be the access-control source for a hosted CMS. Users sign in with GitHub, and the API checks their permission on the configured repository:

```text
GET /repos/{owner}/{repo}/collaborators/{username}/permission
```

Access maps directly from GitHub:

- `admin` -> CMS admin
- `write` or `maintain` -> CMS editor
- `read` or `triage` -> CMS viewer
- `none` or no collaborator record -> no CMS access

In GitHub mode, all git-backed write actions verify the user's current GitHub permission before saving. Users with GitHub edit access can edit documents, folder metadata, scopes, and revisions. Users without edit access can browse and review.

Set these environment variables before starting the FastAPI service:

```bash
export CS_GITHUB_OWNER=jroakes
export CS_GITHUB_REPO=context-system-prototype-codex
export CS_GITHUB_CLIENT_ID=...
export CS_GITHUB_CLIENT_SECRET=...
export CS_PUBLIC_APP_URL=http://127.0.0.1:4321
```

The GitHub OAuth callback URL should point to the FastAPI server:

```text
http://127.0.0.1:8001/api/auth/github/callback
```

When those variables are present, the login screen switches to GitHub sign-in and the local Users screen is hidden.

## Deploying

For a hosted deployment, run the FastAPI service and Astro frontend together with persistent storage for the Git working copy. The backend needs access to:

- The configured `context_repo/` checkout
- `var/users.sqlite` for sessions and local fallback users
- Git credentials that can pull and push the configured repository when GitHub mode is enabled

Use direct commits to the configured branch for the first implementation. Branch protection and pull-request workflows can be added later if we need review gates.

## MCP

The streamable HTTP MCP URL is `http://127.0.0.1:8001/mcp/`. Available tools retrieve constructs, search context, assemble context packages, and validate the bundle.

## CLI

```bash
uv run python run.py validate
uv run python run.py stats
uv run python run.py serve --port 8001
```

## Tests

```bash
uv run pytest
cd cms && npm run build
```
