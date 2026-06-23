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

## Try the Demo

Hosted demo:

[https://context-studio-demo.onrender.com/](https://context-studio-demo.onrender.com/)

Demo login:

```text
demo / demo
```

The hosted demo is read-only and uses synthetic data.

## Run Locally

Requirements:

- Python 3.11+
- Node.js 20+
- `uv`

Start the API:

```bash
git clone https://github.com/locomotive-agency/context-studio.git
cd context-studio
uv sync
uv run python run.py init-demo
uv run python run.py serve --port 8001
```

Start the CMS in a second terminal:

```bash
cd cms
npm install
npm run dev
```

Open:

[http://127.0.0.1:4321](http://127.0.0.1:4321)

Local demo users:

```text
admin / admin123
editor / editor123
viewer / viewer123
```

More setup notes live in [docs/getting-started/README.md](docs/getting-started/README.md).

## Screenshots

### Documents

![Context Studio Documents](demo/screenshots/context-studio-documents.png)

### Collections

![Context Studio Collections](demo/screenshots/context-studio-collections.png)

### MCP Test Tool

![Context Studio MCP Test Tool](demo/screenshots/context-studio-mcp-test-tool.png)

## What It Does

- Stores governed marketing context as Markdown files.
- Uses folder metadata and document frontmatter for scope, type, status, and criticality.
- Keeps curated Documents separate from searchable supporting Collections.
- Avoids semantic search over governed Documents; scoped retrieval is deterministic.
- Uses Collection search only when a surfaced Document or folder points to that Collection.
- Exposes MCP tools for scopes, types, folders, indexes, logs, document metadata, document reads, Collection search, source reads, and validation.
- Provides a browser MCP Test Tool so we can test agent-facing retrieval behavior directly.

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

## Deploy

This repository includes a Render-ready Docker setup and `render.yaml`.

Render deployment notes live in [docs/deploy-to-render/README.md](docs/deploy-to-render/README.md).

## Tests

```bash
uv run pytest
cd cms && npm run build
uv run python run.py validate
```

## Guiding Document

- [MARKETING_CONTEXT_GUIDE.md](MARKETING_CONTEXT_GUIDE.md) explains how marketing context should be structured, governed, retrieved, and separated from skills and outcome specs.
