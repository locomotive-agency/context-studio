# Getting Started

This guide gets a local Context Studio demo running with synthetic data.

## 1. Install Requirements

We use:

- Python 3.11+
- Node.js 20+
- `uv`

## 2. Clone and Seed the Demo

```bash
git clone https://github.com/locomotive-agency/context-studio.git
cd context-studio
uv sync
uv run python run.py init-demo
```

`init-demo` copies tracked synthetic seed files from `demo/context_repo/` into `.local/context_repo/` and seeds the demo Collection from `demo/sample_sources/`.

## 3. Start the API

```bash
uv run python run.py serve --port 8001
```

The API and MCP endpoint run at:

```text
http://127.0.0.1:8001
http://127.0.0.1:8001/mcp/
```

## 4. Start the CMS

In a second terminal:

```bash
cd cms
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:4321
```

## 5. Sign In

Default local users are configured in `config.json`:

```text
admin / admin123
editor / editor123
viewer / viewer123
```

## 6. Try the Core Flows

- Open **Documents** and browse the seeded folders.
- Open a Document and switch between Raw, Preview, and Split.
- Open **Collections** and inspect the seeded sales conversation sources.
- Open **MCP Test Tool** and run `list_context_documents`.
- Run `search_collection` after a scoped Document result surfaces `enterprise-sales-conversations`.
- Open **Validation** and confirm the demo bundle is valid.

## Runtime Data

The source repo keeps code, docs, and demo seed files. Editable runtime data lives outside tracked source paths:

- `demo/context_repo/` is the tracked synthetic seed repository.
- `.local/context_repo/` is the ignored editable local context repository.
- `.local/var/` holds ignored local SQLite databases and Collection source files.

Reset local runtime data:

```bash
uv run python run.py reset-demo
```

## Useful Commands

```bash
uv run python run.py validate
uv run python run.py stats
uv run pytest
cd cms && npm run build
```

## GitHub Access Mode

GitHub can be the access-control source for a hosted CMS. Users sign in with GitHub, and the API checks their permission on the configured repository:

```text
GET /repos/{owner}/{repo}/collaborators/{username}/permission
```

Access maps directly from GitHub:

- `admin` -> CMS admin
- `write` or `maintain` -> CMS editor
- `read` or `triage` -> CMS viewer
- `none` or no collaborator record -> no CMS access

Set these environment variables before starting FastAPI:

```bash
export CS_GITHUB_OWNER=locomotive-agency
export CS_GITHUB_REPO=context-studio
export CS_GITHUB_CLIENT_ID=...
export CS_GITHUB_CLIENT_SECRET=...
export CS_PUBLIC_APP_URL=http://127.0.0.1:4321
```

The GitHub OAuth callback URL should point to the FastAPI server:

```text
http://127.0.0.1:8001/api/auth/github/callback
```

When those variables are present, the login screen switches to GitHub sign-in and the local Users screen is hidden.
