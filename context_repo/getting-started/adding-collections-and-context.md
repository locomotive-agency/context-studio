---
type: reference
title: Adding a new Collection and associating it with context
description: How to create Collections, upload source files, and connect them to governed context.
tags:
- getting-started
- collections
- supporting-sources
- context-packages
---

# Adding a new Collection and associating it with context

Collections hold searchable source material. Use a Collection when the material supports governed context but should not itself become an approved Document.

Examples include call transcripts, interview notes, raw research exports, crawl metadata, and source files used to substantiate a governed record.

## Add a Collection

1. Open Collections.
2. Select New collection.
3. Enter a stable collection ID.
4. Enter a name and description.
5. Select Create.

Use lowercase IDs with hyphens, such as `sales-call-transcripts` or `customer-interviews`.

## Upload source files

1. Select the Collection.
2. Select Upload files.
3. Choose the source files.
4. Wait for each file to show an indexed status.

Indexed files are split into searchable units. Tool Test Bench and context package requests can return cited passages from those units when the Collection is associated with a requested context type.

## Associate a Collection with a context Document

Add `supporting_sources.collections` to a Document frontmatter when that specific Document should use the Collection as supporting evidence.

```yaml
type: audience-profile
title: Sales AEs and SDRs
status: approved
criticality: hybrid
supporting_sources:
  collections:
  - sales-call-transcripts
```

When a Tool Test Bench request asks for `audience-profile` with a query, the response includes approved audience Documents and matching cited passages from `sales-call-transcripts`.

## Associate a Collection with a folder

Add `supporting_sources.collections` to folder metadata when every Document in the folder should inherit the same supporting Collection.

```yaml
type: audience-profile
status: approved
criticality: hybrid
supporting_sources:
  collections:
  - sales-call-transcripts
```

Folder metadata is useful for content areas like `audiences/`, where every audience profile can use the same transcript or interview source Collection.

## Retrieval behavior

Collections are supporting sources, not governed records.

Hybrid and flexible context can return Collection search results when the request includes a query and the requested construct declares supporting Collections.

Controlled context does not use Collection search at runtime. Controlled requests return approved Documents deterministically and block when required controlled context is missing.

## Verify the association

Use Tool Test Bench:

1. Choose the context type associated with the Collection.
2. Enter a query that should match the source material.
3. Run the request.
4. Check that the response includes approved OKF records and Collection results with citations.

If no Collection results appear, confirm the context type, query, Collection ID, and `supporting_sources.collections` metadata.
