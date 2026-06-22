---
type: reference
title: Adding a new Document or Folder
description: How to create governed Documents and folders in the CMS.
tags:
- getting-started
- documents
- folders
- okf
---

# Adding a new Document or Folder

Documents are governed OKF records. Folders organize Documents and can provide inherited metadata through `_schema.yaml`.

## Add a Document

1. Open Documents.
2. Choose the destination folder from the folder list.
3. Select New document.
4. Choose Markdown unless the content is intentionally JSON.
5. Enter a filename without slashes.
6. Enter a title.
7. Choose the context type.
8. Choose a scope when the context should apply to a specific company, brand, product, audience, campaign, channel, or other scope.
9. Select Create.
10. Review the generated frontmatter and body.
11. Save the document.

The CMS writes the file, validates the OKF frontmatter and governance metadata, commits the change to Git, and refreshes the document list.

## Required metadata

Markdown Documents need valid YAML frontmatter. At minimum, every governed Document needs:

```yaml
type: audience-profile
title: Example audience profile
status: approved
```

Most folders inherit `status`, `durability`, `criticality`, and `scope_id` from folder metadata. Document frontmatter can override inherited values when a specific record needs a different type, scope, or governance band.

## Add a Folder

1. Open Documents.
2. Select New folder.
3. Enter the folder path.
4. Select Create.

The CMS creates a folder-level `_schema.yaml` file. A folder can exist before it has Documents because the schema file gives the folder something real to store in Git.

## Set Folder Metadata

Use Folder metadata when every Document in a folder should inherit the same context type, scope, status, durability, criticality, or supporting source settings.

1. Open Folder metadata.
2. Select the folder.
3. Edit the metadata fields or Advanced YAML.
4. Save folder metadata.

Example:

```yaml
type: case-study
status: approved
durability: persistent
criticality: controlled
scope_id: zoominfo
```

## Move Documents Or Folders

Documents can be moved with the Move action or by dragging them into folders. Folders can be reorganized by dragging a folder onto another folder.

Moving a Document or Folder changes its path and commits the move to Git. After a move, inherited folder metadata may change, so check Validation before relying on the moved content.

## Validation

Use Validation after creating or moving content. Common issues are missing `type`, unknown `scope_id`, invalid YAML, or time-bound context without `valid_until`.
