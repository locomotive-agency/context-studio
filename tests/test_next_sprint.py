from __future__ import annotations

from pathlib import Path

from context_system.cms import ContentStore
from context_system.collections import CollectionManager
from context_system.config import Config
from context_system.importer import OKFImporter
from context_system.okf import parse_markdown_metadata
from context_system.repository import ContextRepository
from context_system.service import ContextService


def _config(tmp_path: Path) -> Config:
    return Config(
        context_repository_path=str(tmp_path / "context_repo"),
        audit_path=str(tmp_path / "audit.sqlite"),
        users_path=str(tmp_path / "users.sqlite"),
        collections_root_path=str(tmp_path / "collections"),
        collections_db_path=str(tmp_path / "collections.sqlite"),
    )


def test_controlled_schema_is_discoverable_without_package_assembly(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_schema("", {"type": "legal-and-compliance", "criticality": "controlled"}, "admin")
    service = ContextService(cfg)

    types = service.list_context_types()
    documents = service.list_context_documents(type="legal-and-compliance")

    assert "legal-and-compliance" in types
    assert documents == []


def test_document_metadata_surfaces_supporting_collection_for_agent_search(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_document(
        "audience/sales-leaders.md",
        {
            "type": "audience-profile",
            "title": "Sales leaders",
            "criticality": "hybrid",
            "status": "approved",
            "supporting_sources": {"collections": ["sales-calls"]},
        },
        "Sales leaders care about pipeline quality.",
        "admin",
    )
    collections = CollectionManager(cfg)
    collections.create_collection("sales-calls", "Sales Calls")
    collections.create_collection("excluded", "Excluded")
    document = collections.add_document_text("sales-calls", "call.txt", "renewal risk and pipeline quality came up repeatedly")
    collections.add_document_text("excluded", "excluded.txt", "renewal risk should not appear from this collection")
    service = ContextService(cfg)

    documents = service.list_context_documents(type="audience-profile")
    results = service.search_collection("sales-calls", "renewal risk")

    assert [record["title"] for record in documents] == ["Sales leaders"]
    assert documents[0]["supporting_sources"]["collections"] == ["sales-calls"]
    assert {item["collection_id"] for item in results} == {"sales-calls"}
    assert results[0]["source_title"] == "call.txt"
    assert not Path(results[0]["source_path"]).is_absolute()
    assert not Path(document["source_path"]).is_absolute()
    assert not Path(collections.list_documents("sales-calls")[0]["source_path"]).is_absolute()
    assert "content_hash" in results[0]


def test_controlled_document_metadata_does_not_run_collection_search(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_document(
        "legal/disclaimer.md",
        {
            "type": "legal-and-compliance",
            "title": "Required disclaimer",
            "criticality": "controlled",
            "status": "approved",
            "supporting_sources": {"collections": ["legal-notes"]},
        },
        "Use only the approved disclaimer.",
        "admin",
    )
    collections = CollectionManager(cfg)
    collections.create_collection("legal-notes", "Legal Notes")
    collections.add_document_text("legal-notes", "notes.txt", "renewal risk language in notes")
    service = ContextService(cfg)

    documents = service.list_context_documents(type="legal-and-compliance")

    assert documents
    assert documents[0]["criticality"] == "controlled"
    assert documents[0]["supporting_sources"]["collections"] == ["legal-notes"]


def test_collection_records_have_no_scope_allowed_use_or_summary(tmp_path: Path):
    cfg = _config(tmp_path)
    collections = CollectionManager(cfg)

    created = collections.create_collection("sales-calls", "Sales Calls", description="Discovery calls")

    assert created["id"] == "sales-calls"
    assert "scope_id" not in created
    assert "criticality" not in created
    assert "allowed_use" not in created
    assert "context_types" not in created
    assert not hasattr(collections, "summarize")


def test_folder_and_document_supporting_sources_are_merged(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_schema(
        "audience",
        {
            "type": "audience-profile",
            "criticality": "flexible",
            "supporting_sources": {
                "collections": ["folder-collection"],
                "web": ["https://example.com/folder"],
                "mcp": ["folder-mcp"],
            },
        },
        "admin",
    )
    store.save_document(
        "audience/sales-leaders.md",
        {
            "title": "Sales leaders",
            "supporting_sources": {
                "collections": ["document-collection"],
                "web": ["https://example.com/document"],
                "mcp": ["document-mcp"],
            },
        },
        "Sales leaders context.",
        "admin",
    )

    record = ContextRepository(cfg).get_construct("audience-profile")[0]

    assert record.supporting_sources == {
        "collections": ["folder-collection", "document-collection"],
        "web": ["https://example.com/folder", "https://example.com/document"],
        "mcp": ["folder-mcp", "document-mcp"],
    }


def test_mcp_source_filtering_still_fails_closed_by_role(tmp_path: Path):
    cfg = _config(tmp_path)
    cfg.mcp_servers = [
        {"id": "sales-calls", "roles": ["admin"]},
        {"id": "public-research", "roles": ["viewer", "editor", "admin"]},
    ]
    store = ContentStore(cfg.context_repo)
    store.save_document(
        "audience/sales-leaders.md",
        {
            "type": "audience-profile",
            "title": "Sales leaders",
            "criticality": "flexible",
            "status": "approved",
            "supporting_sources": {"mcp": ["sales-calls", "public-research"]},
        },
        "Sales leaders context.",
        "admin",
    )
    service = ContextService(cfg)

    allowed, denied = service._rbac_mcp_sources(["sales-calls", "public-research"], {"username": "viewer", "role": "viewer"})

    assert allowed == ["public-research"]
    assert denied == [{"kind": "mcp", "value": "sales-calls", "reason": "insufficient role"}]


def test_missing_user_context_does_not_default_to_admin(tmp_path: Path):
    cfg = _config(tmp_path)
    cfg.mcp_servers = [{"id": "admin-source", "roles": ["admin"]}]
    service = ContextService(cfg)

    allowed, denied = service._rbac_mcp_sources(["admin-source"], user=None)

    assert allowed == []
    assert denied == [{"kind": "mcp", "value": "admin-source", "reason": "missing authenticated user"}]


def test_markdown_metadata_extracts_links_citations_and_headings():
    metadata = parse_markdown_metadata(
        "# Positioning\n\n"
        "Use [Messaging](../brand/messaging.md) with [external proof](https://example.com/proof).\n\n"
        "## Citations\n\n"
        "- [Customer Study](https://example.com/customer-study)\n"
    )

    assert metadata.headings == [
        {"level": 1, "text": "Positioning"},
        {"level": 2, "text": "Citations"},
    ]
    assert metadata.internal_links == [{"text": "Messaging", "target": "brand/messaging.md"}]
    assert {"text": "external proof", "target": "https://example.com/proof"} in metadata.external_links
    assert {"text": "Customer Study", "target": "https://example.com/customer-study"} in metadata.citations


def test_runtime_records_include_structured_links_and_citations(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_document(
        "audience/sales-leaders.md",
        {
            "type": "audience-profile",
            "title": "Sales leaders",
            "criticality": "hybrid",
            "status": "approved",
        },
        "# Sales Leaders\n\nSee [Proof](../proof/customer.md).\n\n## Citations\n\n- [Source](https://example.com/source)",
        "admin",
    )

    record = ContextRepository(cfg).get_construct("audience-profile")[0]

    assert record.headings == [{"level": 1, "text": "Sales Leaders"}, {"level": 2, "text": "Citations"}]
    assert record.links == [{"text": "Proof", "target": "proof/customer.md"}]
    assert record.citations == [{"text": "Source", "target": "https://example.com/source"}]


def test_okf_traversal_reads_index_log_and_concepts(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    (cfg.context_repo / "proof").mkdir(parents=True)
    (cfg.context_repo / "proof" / "index.md").write_text("# Proof Index\n\nSee [Customer](customer.md).", encoding="utf-8")
    (cfg.context_repo / "proof" / "log.md").write_text("# Proof Log\n\n- Added customer proof.", encoding="utf-8")
    store.save_document(
        "proof/customer.md",
        {
            "type": "proof-points",
            "title": "Customer Proof",
            "status": "approved",
            "custom_okf_key": "preserved",
        },
        "# Customer Proof\n\nSee [Index](index.md).\n\n## Citations\n\n- [Proof](https://example.com/proof)",
        "admin",
    )

    entries = store.list_okf_entries("proof")
    index = store.read_okf_index("proof")
    log = store.read_okf_log("proof")
    concept = store.read_okf_entry("proof/customer.md")

    assert {entry["path"] for entry in entries} == {"proof/customer.md", "proof/index.md", "proof/log.md"}
    customer_entry = next(entry for entry in entries if entry["path"] == "proof/customer.md")
    assert customer_entry["links"] == [{"text": "Index", "target": "proof/index.md"}]
    assert customer_entry["citations"] == [{"text": "Proof", "target": "https://example.com/proof"}]
    assert index["kind"] == "index"
    assert index["links"] == [{"text": "Customer", "target": "proof/customer.md"}]
    assert log["kind"] == "log"
    assert concept["kind"] == "concept"
    assert concept["effective_frontmatter"]["custom_okf_key"] == "preserved"


def test_scoped_document_metadata_surfaces_effective_collection_sources(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_scope({"id": "global", "name": "Global", "level": "company"}, "admin")
    store.save_scope({"id": "enterprise", "name": "Enterprise", "level": "audience", "parent_id": "global"}, "admin")
    store.save_schema(
        "audience",
        {
            "type": "audience-profile",
            "criticality": "hybrid",
            "supporting_sources": {"collections": ["global-research"]},
        },
        "admin",
    )
    store.save_document(
        "audience/sales-leaders.md",
        {"title": "Sales leaders", "status": "approved"},
        "Sales leaders care about pipeline quality.",
        "admin",
    )
    store.save_document(
        "audience/enterprise-sales-leaders.md",
        {
            "title": "Enterprise sales leaders",
            "status": "approved",
            "scope_id": "enterprise",
            "supporting_sources": {"collections": ["enterprise-research"]},
        },
        "Enterprise sales leaders care about renewal risk.",
        "admin",
    )
    collections = CollectionManager(cfg)
    collections.create_collection("global-research", "Global Research")
    collections.create_collection("enterprise-research", "Enterprise Research")
    collections.add_document_text("global-research", "global.txt", "renewal risk appears in global context")
    collections.add_document_text("enterprise-research", "enterprise.txt", "renewal risk appears in enterprise context")
    service = ContextService(cfg)

    global_documents = service.list_context_documents(type="audience-profile", scope_id="global")
    enterprise_documents = service.list_context_documents(type="audience-profile", scope_id="enterprise")
    global_results = service.search_collection("global-research", "renewal risk")
    enterprise_results = service.search_collection("enterprise-research", "renewal risk")

    assert {doc["title"] for doc in global_documents} == {"Sales leaders"}
    assert {doc["title"] for doc in enterprise_documents} == {"Sales leaders", "Enterprise sales leaders"}
    assert global_documents[0]["supporting_sources"]["collections"] == ["global-research"]
    assert {item["collection_id"] for item in global_results} == {"global-research"}
    assert {item["collection_id"] for item in enterprise_results} == {"enterprise-research"}


def test_document_listing_does_not_search_collections(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_document(
        "audience/sales-leaders.md",
        {
            "type": "audience-profile",
            "title": "Sales leaders",
            "criticality": "hybrid",
            "status": "approved",
            "supporting_sources": {"collections": ["sales-calls"]},
        },
        "Sales leaders care about pipeline quality.",
        "admin",
    )
    collections = CollectionManager(cfg)
    collections.create_collection("sales-calls", "Sales Calls")
    collections.add_document_text("sales-calls", "call.txt", "renewal risk and pipeline quality came up repeatedly")
    service = ContextService(cfg)

    documents = service.list_context_documents(type="audience-profile")

    assert documents[0]["supporting_sources"]["collections"] == ["sales-calls"]
    assert "collection_results" not in documents[0]


def test_okf_folder_import_preserves_files_and_commits_once(tmp_path: Path):
    cfg = _config(tmp_path)
    source = tmp_path / "okf_source"
    (source / "proof").mkdir(parents=True)
    (source / "proof" / "_schema.yaml").write_text("type: proof-points\ncriticality: hybrid\n", encoding="utf-8")
    (source / "proof" / "index.md").write_text("# Proof\n", encoding="utf-8")
    (source / "proof" / "log.md").write_text("# Log\n", encoding="utf-8")
    (source / "proof" / "customer.md").write_text(
        "---\ntitle: Customer Proof\nstatus: approved\n---\n\nProof body.\n",
        encoding="utf-8",
    )
    importer = OKFImporter(cfg)

    plan = importer.scan(source)
    result = importer.apply(plan, author="admin")

    assert plan["blockers"] == []
    assert (cfg.context_repo / "proof" / "_schema.yaml").is_file()
    assert (cfg.context_repo / "proof" / "index.md").is_file()
    assert (cfg.context_repo / "proof" / "log.md").is_file()
    assert (cfg.context_repo / "proof" / "customer.md").is_file()
    assert result["imported_files"] == [
        "proof/_schema.yaml",
        "proof/customer.md",
        "proof/index.md",
        "proof/log.md",
    ]
    assert len(ContentStore(cfg.context_repo).git.history()) == 1
