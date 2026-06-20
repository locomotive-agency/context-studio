---
type: reference
title: Getting started
description: How we run the context CMS locally and understand the main workspace areas.
tags:
- getting-started
- cms
- local-development
---

# Getting started

This guide explains how we run the context CMS locally and what each main area does.

## Start the API

From the project root:

```bash
uv sync
uv run python run.py serve --port 8001
```

The API serves the CMS data endpoints and the MCP endpoint.

## Start the CMS

In a second terminal:

```bash
cd cms
npm install
npm run dev
```

Open `http://127.0.0.1:4321`.

## Sign in locally

When GitHub mode is not configured, the CMS uses local demo accounts:

- `admin` / `admin123`
- `editor` / `editor123`
- `viewer` / `viewer123`

## Main workspace areas

Documents is where we browse, create, edit, preview, and delete context files.

Validation shows files that are not valid OKF or do not meet governance rules.

History shows Git revisions. Repository history shows structural changes. Document history shows revisions for the open document and supports restore.

Scopes defines the hierarchy used to align context to company, brand, product, campaign, audience, and similar levels.

Schemas manages folder metadata. Documents inherit folder metadata, and document frontmatter can override it.

Users is available in local mode. In GitHub mode, access is managed from GitHub repository permissions.

## Create a document

1. Choose a folder in Documents.
2. Select New document.
3. Select the folder and enter a filename.
4. Add a title, type, and optional scope.
5. Save the document.

The CMS writes the file, validates it as OKF, and commits the change to Git.

## Create a folder

Use New folder from Documents or Folder metadata. A folder is represented by a folder-level `_schema.yaml` file, so it can hold inherited metadata even before it has documents.

Folders can be deleted only when they contain no documents.
