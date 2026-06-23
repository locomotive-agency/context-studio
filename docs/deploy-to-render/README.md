# Deploy to Render

Context Studio can run on Render as one Docker web service. The Docker build compiles the Astro CMS and serves the static bundle from FastAPI, so the public app, `/api/*`, and `/mcp/*` share one origin.

## Current Demo

Public demo:

```text
https://context-studio-demo.onrender.com/
```

Demo login:

```text
demo / demo
```

The public demo is read-only and uses synthetic data.

## Included Files

- `Dockerfile` builds the CMS and API into one image.
- `render.yaml` defines the Render web service.
- `.dockerignore` keeps local runtime data and build artifacts out of the image.

## Free Read-Only Demo

The checked-in `render.yaml` is configured for a free Render web service:

- Docker runtime
- `/api/health` health check
- generated `CS_SECRET_KEY`
- `demo / demo` viewer user
- synthetic demo data seeded on boot

Free Render web services do not support persistent disks. That is acceptable for a read-only demo because viewer users cannot edit content.

## Editable Hosted Demo

For an editable hosted demo, use a paid Render instance type and attach a persistent disk mounted at `/var/data`.

Set these environment variables:

```bash
CS_SECRET_KEY=replace-with-a-long-random-value
CS_PUBLIC_APP_URL=https://your-context-app.example.com
CS_CONTEXT_REPOSITORY_PATH=/var/data/context_repo
CS_USERS_PATH=/var/data/users.sqlite
CS_AUDIT_PATH=/var/data/audit.sqlite
CS_COLLECTIONS_ROOT_PATH=/var/data/collections
CS_COLLECTIONS_DB_PATH=/var/data/collections.sqlite
```

For GitHub login and Git-backed production editing, also set:

```bash
CS_GITHUB_OWNER=locomotive-agency
CS_GITHUB_REPO=context-studio
CS_GITHUB_CLIENT_ID=...
CS_GITHUB_CLIENT_SECRET=...
```

The GitHub OAuth callback URL should be:

```text
https://your-context-app.example.com/api/auth/github/callback
```

## Deploy From the Dashboard

1. Push the repo to GitHub.
2. In Render, create a new web service from the GitHub repo.
3. Choose Docker as the runtime.
4. Use `./Dockerfile`.
5. Set the health check path to `/api/health`.
6. Add the environment variables above.
7. Deploy.

## Verify

```bash
curl https://your-context-app.example.com/api/health
```

Then sign in through the public URL and run a request in **MCP Test Tool**.

## Notes

If GitHub mode is enabled, the deployed working copy needs an `origin` remote and Git credentials that can pull and push the configured branch. Writes use direct commits, pull with `--ff-only` before saving, and push after each successful Git-backed write.
