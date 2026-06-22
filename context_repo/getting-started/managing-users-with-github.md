---
type: reference
title: Managing users with GitHub
description: How GitHub repository permissions control login and edit access in hosted mode.
tags:
- getting-started
- github
- access-control
---

# Managing users with GitHub

In hosted mode, GitHub is the source of truth for CMS access.

Users cannot enter the CMS unless they have access to the configured GitHub repository. Repository admins can manage governed structure and content. Users with GitHub edit-level access can edit document folders, documents, and Collections. Users with read-level access can review and request context without editing.

## Permission mapping

The API checks:

```text
GET /repos/{owner}/{repo}/collaborators/{username}/permission
```

GitHub permissions map to CMS access like this:

| GitHub permission | CMS access |
| --- | --- |
| `admin` | Admin |
| `maintain` | Editor |
| `write` | Editor |
| `triage` | Viewer |
| `read` | Viewer |
| `none` or missing access | No access |

## Add a user

1. Open the repository in GitHub.
2. Add the person as a collaborator or grant access through a GitHub team.
3. Choose the GitHub permission level.
4. Ask the user to sign in to the CMS with GitHub.

The CMS does not need a separate user record in GitHub mode.

## Remove a user

Remove the user's repository access in GitHub. The next permission check will prevent access or editing.

## Edit access

Before each write action, the CMS re-checks the user's GitHub permission.

Admin write actions include:

- Editing folder metadata schemas
- Creating, editing, moving, or deleting scopes
- Importing OKF folders

Editor write actions include:

- Creating, editing, deleting, or restoring documents
- Creating or deleting folders
- Creating Collections and uploading Collection source files

If GitHub no longer grants edit access, the write is blocked.

## Local mode

When GitHub settings are not configured, the CMS uses the local demo users configured in `config.json` and stored in SQLite. Local mode is useful for development and review, but GitHub mode is the intended hosted access model.
