# Context Documentation System Prototype

This prototype is a file-based context CMS for OKF context documents plus searchable supporting Collections. Astro provides the CMS interface. FastAPI and Pydantic handle authentication, filesystem operations, OKF validation, scoped retrieval, Git history, Collection indexing, context package assembly, and MCP access. FastMCP exposes valid context to AI tools.

## What It Does

- Stores Markdown OKF records and JSON source files in `context_repo/`
- Uses local Git for commits, history, diffs, restores, and deletes
- Supports folder-level metadata inherited by documents
- Lets document frontmatter override folder metadata
- Validates documents for OKF and governance rules
- Provides Raw, Preview, and Split document views
- Imports OKF folders into `context_repo/`
- Stores supporting source files in Collections
- Indexes Collection passages with SQLite FTS5 and a local deterministic embedding vector
- Returns cited Collection passages for hybrid and flexible context when routed by OKF supporting sources
- Provides a Tool Test Bench for calling the real context package endpoint
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

CMS creation and editing actions use right-side drawers. Documents can be added, edited, deleted, restored, and inspected through Git history. Folders can be added and deleted when empty. Admins can edit users and everything else. Editors can edit Folders, Documents, and Collections. Viewers can request context and semantic data. In GitHub mode, user access is managed in GitHub repository settings.

Markdown files are validated as OKF records. JSON files are supported as structured source documents. Both formats provide Raw, Preview, and Split editor modes. Representative case study, competitive, and ICP examples live under `context_repo/examples/`.

## Context Model

The project separates curated context from supporting source material.

- **Documents** are OKF records in `context_repo/`. They are retrieved deterministically by fields like `type`, `scope_id`, `status`, `criticality`, and `valid_until`.
- **Collections** are local buckets of source files under `var/collections/`. They store original source documents and indexed retrieval units. They are not OKF records.
- **Tool Test Bench** calls the same context package endpoint used by AI workflows and MCP clients.

OKF records are never retrieved with semantic embeddings. Collection retrieval is available only when a matching OKF document or inherited folder schema points to that Collection through `supporting_sources.collections`.

Supporting source shape:

```yaml
supporting_sources:
  collections:
    - collection-1
  web:
    - https://example.com/page
  mcp:
    - sales-calls
```

Controlled context ignores supporting sources. Hybrid and flexible context can include approved OKF records, cited Collection passages, and suggested web/MCP sources.

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

In GitHub mode, all git-backed write actions verify the user's current GitHub permission before saving. Repository admins can edit scopes and content in the app, while user access is managed in GitHub. GitHub users with `write` or `maintain` access can edit Folders, Documents, and Collections. GitHub users with `read` or `triage` access can request context and semantic data.

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

Use direct commits to the configured branch for the first implementation.

## MCP

The streamable HTTP MCP URL is `http://127.0.0.1:8001/mcp/`. MCP access requires a valid local or GitHub login. Available tools retrieve constructs, assemble context packages, and validate the bundle.

## API Highlights

- `POST /api/context-package` assembles the v1 context package contract.
- `POST /api/imports/okf-folder/scan` scans an OKF folder before import.
- `POST /api/imports/okf-folder/apply` imports an OKF folder as one Git-backed operation.
- `GET /api/collections` lists Collections.
- `POST /api/collections` creates a Collection with only ID, name, and description.
- `POST /api/collections/{collection_id}/documents` stores and indexes a source document.

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
