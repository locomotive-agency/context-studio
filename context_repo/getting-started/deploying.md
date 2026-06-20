---
type: reference
title: Deploying
description: How we deploy the CMS with persistent Git-backed storage and GitHub access control.
tags:
- getting-started
- deployment
- github
---

# Deploying

The hosted CMS needs the Astro frontend, the FastAPI service, and a persistent Git working copy.

## Runtime pieces

The deployment runs:

- Astro frontend for the browser UI
- FastAPI backend for CMS APIs
- FastMCP mounted at `/mcp/`
- A local checkout of the context repository
- SQLite for sessions and lightweight local state

## Required persistence

The backend must retain:

- `context_repo/`
- `var/users.sqlite`
- Any Git credentials or environment configuration needed by the host

The Git working copy is important because the CMS uses Git for history, diffs, restore, backup, and sync.

## GitHub settings

Set these environment variables for GitHub access mode:

```bash
export CS_GITHUB_OWNER=jroakes
export CS_GITHUB_REPO=context-system-prototype-codex
export CS_GITHUB_CLIENT_ID=...
export CS_GITHUB_CLIENT_SECRET=...
export CS_PUBLIC_APP_URL=https://your-cms-host.example.com
```

The GitHub OAuth callback should point to the backend:

```text
https://your-api-host.example.com/api/auth/github/callback
```

For local testing, the callback is:

```text
http://127.0.0.1:8001/api/auth/github/callback
```

## Git sync behavior

In GitHub mode, the backend:

1. Pulls from `origin` on startup.
2. Checks the signed-in user's GitHub repository permission before a write.
3. Runs `git pull --ff-only` before saving.
4. Commits the changed path.
5. Pushes to the current branch.

If the pull cannot fast-forward, the write is blocked so we do not overwrite remote changes.

## Branch model

The simple deployment model commits directly to the configured branch. This keeps editing fast and keeps Git history visible in the CMS.

If we later need review gates, GitHub branch protection can be added, but that should be handled intentionally because it changes the save workflow.

## Health check

The backend health endpoint is:

```text
GET /api/health
```

The response includes the MCP URL path.
