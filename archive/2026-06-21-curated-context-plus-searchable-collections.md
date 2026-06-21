# Archived Sprint: Curated Context Plus Searchable Collections

Archived on: 2026-06-21

Original document: `NEXT_SPRINT.md`

Status: implemented and archived. Remaining policy and hardening work is rolled into the new `NEXT_SPRINT.md`.

## Completion Checklist

- [x] Context package v1 request and response contract exists at `/api/context-package`.
- [x] Criticality is resolved by repository rules rather than by the request payload.
- [x] Missing controlled context blocks the context package response.
- [x] Controlled context returns deterministic approved OKF records only.
- [x] Hybrid and flexible context can return approved OKF records plus cited Collection passages.
- [x] OKF folder import has scan and apply flows.
- [x] Import preserves folder structure and commits accepted files as one Git revision.
- [x] Collections are separate from OKF Documents.
- [x] Collections store original source files under `var/collections/<collection_id>/sources/`.
- [x] Collection metadata excludes scope, criticality, context type, and allowed-use settings.
- [x] Collection parsing uses MarkItDown when available.
- [x] No summarization feature was added for Collections.
- [x] Collection indexing creates SQLite FTS entries and local embedding vectors.
- [x] Collection retrieval returns cited passages.
- [x] OKF records are not searched semantically.
- [x] Document and folder `supporting_sources` pointers support Collections, web resources, and MCP servers.
- [x] Controlled context ignores supporting sources.
- [x] Tool Test Bench calls the real context package endpoint.
- [x] Backend tests cover controlled blocking, Collection routing, MCP source filtering, OKF import, no OKF semantic retrieval, and no Collection summarization API.

## Remaining Or Rolled Forward

- [ ] Make the MCP/API access policy explicit in code and tests: data access requires a logged-in local or GitHub user.
- [ ] Align role language with the product policy: Admins manage users and everything, Editors manage Folders/Documents/Collections, and Viewers request context and semantic data.
- [ ] Add production retrieval improvements later: stronger local embedding model, optional local vector store, indexing progress, and reindex controls.
- [ ] Add MCP source registry hardening: config validation and clearer unavailable-source reporting in the Tool Test Bench.

## Validation Evidence

- `uv run pytest` passed with 29 tests and 1 upstream Starlette/httpx deprecation warning.
- `npm run build` passed with 0 Astro errors, warnings, or hints.
- `git status --short` was clean before archiving.

## Original Sprint Document

# Next Sprint: Curated Context Plus Searchable Collections

## Core Idea

The system has two separate kinds of context.

1. **Curated OKF records**
   These live in `context_repo/`. They are retrieved by deterministic fields like `type`, `scope_id`, `criticality`, `status`, and `valid_until`. They are not retrieved with embeddings.

2. **Collections**
   These are buckets of source documents that users can drop files into for retrieval. Collections store the original source documents, index them, and return cited passages. They do not become OKF records.

Plain-language model:

```text
Documents = approved context records
Collections = searchable supporting sources
Tool Test Bench = try the same requests an AI workflow will make
```

## Sprint Goal

Build the first version of a useful context workbench:

- Define the context package request and response contract.
- Import existing OKF folders into the Documents knowledgebase.
- Add a separate Collections area where users can drop supporting files and index them.
- Support BM25 plus local embedding retrieval over Collections.
- Let Documents and folders point to supporting sources: Collections, web resources, or MCP servers.
- Add a Tool Test Bench so users can call the real tools with test requests and inspect responses.

## Priority 0: Context Package Contract

### What Changes

Define the request and response shape before changing retrieval.

Request:

```json
{
  "task": "campaign brief",
  "scope_id": "product-a",
  "requests": [
    {
      "type": "audience-profile",
      "query": "buyer pains for sales leaders"
    }
  ]
}
```

Response:

```json
{
  "task": "campaign brief",
  "scope_id": "product-a",
  "results": [
    {
      "type": "audience-profile",
      "resolved_criticality": "hybrid",
      "okf_records": [],
      "collection_results": [],
      "suggested_sources": [],
      "missing": []
    }
  ],
  "blocked": false,
  "kb_git_sha": "..."
}
```

Rules:

- The request names the context `type`, scope, task, and optional query. It does not send criticality.
- The service resolves criticality from the system's rules for the matching context type and scope.
- The resolver must work even when no OKF record exists, so missing controlled context can still block correctly.
- Resolution can come from construct defaults, inherited folder/schema rules, or another system-maintained type/scope policy. It should not come from the user request.
- Controlled results return approved OKF records only.
- Missing controlled context blocks the run.
- Hybrid results return approved OKF records plus eligible Collection results.
- Flexible results may return OKF records, Collection results, and suggested sources.
- OKF records and Collection results stay in separate fields.
- The response reports `resolved_criticality` so the user and AI workflow can see which behavior was applied.

### Why

The current service accepts only a list of constructs and returns flat `records` and `search_pointers`. The new contract makes the important behavior enforceable: controlled context is deterministic; hybrid and flexible context can include supporting retrieval.

## Priority 1: OKF Folder Import

### What Changes

Add a first-class import flow for folders that already contain OKF files.

Backend:

- Add `importer.scan(source_folder)` and `importer.apply(import_plan)`.
- Detect markdown OKF records, JSON source files, `_schema.yaml`, `_scopes.yaml`, `index.md`, and `log.md`.
- Validate OKF frontmatter and governance fields.
- Validate duplicate IDs, duplicate paths, unknown scopes, expired records, and scope conflicts.
- Preserve folder structure.
- Copy accepted files into `context_repo/`.
- Commit the import as one Git revision.
- Do not loop through existing single-file save APIs, because those commit one file at a time.

CMS:

- Add **Import OKF Folder** under Documents.
- Show one import report:
  - blockers first
  - warnings second
  - file list collapsed by default
- Allow import only after blockers are resolved.

### Why

If a user has a folder of OKF records, the app should add it as a knowledgebase. It should not treat those files as raw source documents, summarize them, or index them as Collection material.

## Priority 2: Collections

### What Changes

Add a separate **Collections** section.

A Collection is a bucket where users can drop files that should be searchable as supporting context.

Backend:

- Add `collections_root`, defaulting to `var/collections/`.
- Add `collections_db`, defaulting to `var/collections.sqlite`.
- When files are added, copy them into:

```text
var/collections/<collection_id>/sources/
```

- Store the original source documents.
- Store file hashes, original filenames, stored paths, MIME/file type, modified time, and index status.
- Use Microsoft's MarkItDown as the parser so Collections can accept the full set of formats MarkItDown supports.
- Parse source documents into natural retrieval units:
  - markdown heading sections
  - text paragraphs
  - document pages or sections when the parser exposes them
- Do not summarize.
- Do not add summarization functionality.
- Do not create OKF records.

CMS:

- Add a top-level **Collections** area.
- Let users create a collection with:
  - name
  - description
- Let users drop files into the collection.
- Show source documents, indexing status, errors, and last indexed time.
- Do not ask for collection scope, criticality, context type, or allowed use.
- All usage rules route through OKF Documents and folders that point to the Collection as a supporting source.

Internal tables:

- `collections`
- `collection_documents`
- `collection_units`
- `collection_units_fts`
- `collection_unit_embeddings`
- `collection_errors`

### Why

This handles the "500 similar files" case. Sales transcripts, campaign notes, interview files, and competitive research should be searchable without becoming 500 OKF records.

## Priority 3: Collection Retrieval

### What Changes

Add retrieval over Collections only.

Do not run semantic retrieval over OKF records.

Retrieval stack:

- **BM25/keyword:** SQLite FTS5.
- **Embeddings/vector:** local open-source model plus local vector store.
- Preferred vector store: Qdrant running locally.
- Preferred local embedding model candidate: `Qwen/Qwen3-Embedding-0.6B-GGUF` via llama.cpp or Ollama.
- Stable fallback candidate: `BAAI/bge-m3`.
- Model choice should be config-driven.

Indexing:

- Each retrieval unit gets:
  - unit ID
  - collection ID
  - source document ID
  - source path
  - heading/page/paragraph label
  - text
  - content hash
  - BM25 index entry
  - embedding vector

Search:

- Resolve OKF context first.
- If resolved criticality is `controlled`, do not search Collections.
- If resolved criticality is `hybrid` or `flexible`, collect eligible Collection IDs from the matching OKF Document or inherited folder `supporting_sources.collections`.
- Search only those Collections.
- If no OKF Document or folder points to a Collection, do not search Collections.
- Collections do not have scope, criticality, context type, or allowed-use settings.
- Run BM25 search.
- Run embedding search.
- Merge results with a simple rank merge.
- Return cited passages.

Citation shape:

```json
{
  "collection_id": "sales-transcripts",
  "source_document_id": "doc_123",
  "source_title": "Discovery Call - Acme - 2026-04-12.txt",
  "source_path": "var/collections/sales-transcripts/sources/...",
  "location": "paragraph 18",
  "unit_id": "doc_123#p18",
  "content_hash": "..."
}
```

### Why

Collections are where similarity search belongs. They are unstructured supporting sources. OKF records are already structured and should be retrieved deterministically.

## Priority 4: Supporting Source Pointers

### What Changes

Documents and folders should be able to point to supporting sources that are useful for hybrid or flexible context.

Add minimal metadata that can live in document frontmatter or inherited folder schema:

```yaml
supporting_sources:
  collections:
    - collection-1
    - collection-2
  web:
    - https://example.com/page
  mcp:
    - sales-calls
    - https://example.com/mcp
```

Rules:

- These pointers are not canonical truth.
- They are available only for hybrid and flexible context.
- Controlled requests ignore them.
- Folder-level pointers are inherited by documents.
- Document-level pointers can add to folder-level pointers.
- MCP pointers name supported MCP servers or MCP server URLs, not individual tools.
- MCP access must enforce RBAC before a server is returned in a response or used by the app.
- If the current user or workflow cannot access a configured MCP server, omit it from available supporting sources and report the access issue in the Tool Test Bench.

CMS:

- In Documents and folder metadata, show a **Supporting Sources** section.
- Let users attach:
  - Collection
  - web resource
  - MCP server
- Show these as options in the Tool Test Bench and context package response.

### Why

This gives the system a clean way to say, "For this kind of context, useful supporting material may live over there," without turning that material into OKF records or governance metadata.

## Priority 5: Tool Test Bench

### What Changes

Replace the vague "preview" idea with a screen that calls the real tools.

CMS:

- Add **Tool Test Bench**.
- Let users build a test request:
  - task
  - scope
  - context types
  - optional query
- Call the same backend endpoint used by MCP/API.
- Show:
  - request JSON
  - response JSON
  - Approved context
  - Collection passages with citations
  - suggested web/MCP sources
  - missing controlled context
  - blocked/not blocked status
  - RBAC issues for supporting MCP servers
- Default to blockers and attention-needed items first.

### Why

Users need to test what an AI workflow will actually receive. This screen is not a mock preview; it is a safe way to call the tools with test inputs and inspect the real response.

## Priority 6: Context Package Assembly

### What Changes

Update assembly behavior around the new contract.

Controlled:

- Deterministic OKF lookup only.
- Return approved, current OKF records matching type and scope.
- If missing, return a blocking missing-context result.
- Ignore Collections, web pointers, and MCP pointers.

Hybrid:

- Deterministic OKF lookup.
- Search Collections named in matching OKF `supporting_sources.collections` if a query is present.
- Include web/MCP pointers as suggested sources after RBAC checks.
- Do not block if supporting retrieval finds nothing.

Flexible:

- Return OKF records if available.
- Search Collections named in matching OKF `supporting_sources.collections` if a query is present.
- Include web/MCP pointers as suggested sources after RBAC checks.
- Do not block if nothing is found.

### Why

This is the actual behavior MCP clients and AI workflows need.

## Acceptance Criteria

- An admin can import a valid OKF folder into `context_repo/` with one Git commit.
- A user can create a Collection and drop source files into it.
- Source documents are stored in the Collection.
- Collection parsing uses MarkItDown-supported formats.
- No summarization feature is added.
- Collection indexing creates BM25 entries and embedding vectors.
- Collection retrieval returns cited passages.
- Documents and folders can point to supporting Collections, web resources, and MCP servers.
- Collections do not carry scope, criticality, context type, or allowed-use settings.
- Collection retrieval is allowed only through OKF Document or folder supporting-source pointers.
- MCP supporting sources enforce RBAC.
- Controlled context requests never search Collections or suggested sources.
- Hybrid/flexible requests can return OKF records plus cited Collection passages.
- The Tool Test Bench can call the real context package endpoint and show the actual response.

## Files Likely To Change

Backend:

- `context_system/models.py`
- `context_system/config.py`
- `context_system/cms.py`
- `context_system/repository.py`
- `context_system/service.py`
- `context_system/app.py`
- new `context_system/importer.py`
- new `context_system/collections.py`
- new `context_system/retrieval.py`

Frontend:

- `cms/src/pages/index.astro`
- `cms/src/styles/global.css`

Tests:

- `tests/test_context_service.py`
- new `tests/test_importer.py`
- new `tests/test_collections.py`
- new `tests/test_retrieval.py`
- new `tests/test_context_package.py`

Docs:

- `README.md`
- `PLAN.md`

## Sources Reviewed

- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Google OKF spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [Marketing context spec](C:/Users/jroak/Downloads/structuring-marketing-context-for-ai-improved.md)
- [Qdrant documentation](https://qdrant.tech/documentation/)
- [Qwen3 Embedding 0.6B GGUF model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF)
- [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3)
- Current repo implementation in `context_system/`, `context_repo/`, and `cms/`
