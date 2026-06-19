# Context Documentation System Prototype

This prototype is a file-based context CMS. Astro provides document, scope, schema, history, validation, and user management. FastAPI and Pydantic handle authentication, filesystem operations, OKF validation, scoped retrieval, and local Git history. FastMCP exposes the same valid context to AI tools.

## Storage

`context_repo/` is a standalone local Git repository. CMS writes create commits in that repository; no GitHub remote or deployment workflow is required.

Governance resolves in this order:

1. `context_repo/_schema.yaml`
2. Each nested folder's `_schema.yaml`
3. The document's YAML frontmatter

Later values override earlier values. Every concept document must still contain its own OKF `type` field.

`context_repo/_scopes.yaml` stores the parent-linked scope hierarchy. Documents use a `scope_id`; context retrieval inherits from parent scopes and prefers the most specific matching records.

CMS creation and editing actions use right-side drawers. Administrators can add, edit, and remove users and scopes. The active user and final administrator account cannot be removed.

## Run

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

Default local users:

- `admin` / `admin123`
- `editor` / `editor123`
- `viewer` / `viewer123`

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
