# Context Studio

Context Studio is a file-based context CMS for governed marketing Documents plus searchable supporting Collections. We use plain folders, Markdown, YAML frontmatter, SQLite, and Git so teams can inspect, edit, validate, and retrieve AI context without a heavy knowledge-platform stack.

The system is intentionally simple:

- **Documents** are OKF-style Markdown records in a normal folder tree.
- **Collections** are source-file buckets indexed locally for cited retrieval.
- **Git** provides history, diffs, restore, and backup.
- **SQLite** stores users, audit events, and Collection indexes.
- **FastAPI** serves the API, MCP endpoint, and production CMS bundle.
- **Astro** provides the browser UI.
- **Docker/Render** can host the demo as one web service.

## What It Does

- Stores governed marketing context as Markdown files.
- Uses folder metadata and document frontmatter for scope, type, status, and criticality.
- Keeps curated Documents separate from searchable supporting Collections.
- Avoids semantic search over governed Documents; scoped retrieval is deterministic.
- Uses Collection search only when a surfaced Document or folder points to that Collection.
- Exposes MCP tools for scopes, types, folders, indexes, logs, document metadata, document reads, Collection search, source reads, and validation.
- Provides a browser MCP Test Tool so we can test agent-facing retrieval behavior directly.

## Context Solution Guide

[Marketing_Context.md](Marketing_Context.md) explains the larger marketing-team context model behind this prototype: how context should be structured, governed, retrieved, and separated from skills and outcome specs.

## Try the Demo

Hosted demo:

[https://context-studio-demo.onrender.com/](https://context-studio-demo.onrender.com/)

Demo logins:

```text
admin / admin123
editor / editor123
viewer / viewer123
```

The hosted demo uses synthetic data. Edits are useful for testing but should be treated as ephemeral on the free Render service.

## Run It Yourself

Local setup:

[docs/getting-started.md](docs/getting-started.md)

Render deployment:

[docs/deploy-to-render.md](docs/deploy-to-render.md)

## Screenshots

### Documents

![Context Studio Documents](demo/screenshots/context-studio-documents.png)

### Collections

![Context Studio Collections](demo/screenshots/context-studio-collections.png)

### MCP Test Tool

![Context Studio MCP Test Tool](demo/screenshots/context-studio-mcp-test-tool.png)

## Demo Data

The tracked `demo/` folder contains synthetic demo assets:

- `demo/context_repo/` contains governed marketing Documents for the Context Studio demo brand.
- `demo/sample_sources/` contains synthetic transcript files for Collection seeding.
- `demo/screenshots/` contains README screenshots.

Editable runtime data is ignored by Git and lives under `.local/` by default.

Reset local demo data:

```bash
uv run python run.py reset-demo
```

## Tests

```bash
uv run pytest
cd cms && npm run build
uv run python run.py validate
```
