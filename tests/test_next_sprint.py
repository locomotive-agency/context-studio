from __future__ import annotations

from pathlib import Path

from context_system.cms import ContentStore
from context_system.collections import CollectionManager
from context_system.config import Config
from context_system.importer import OKFImporter
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


def test_context_package_blocks_missing_controlled_context_from_schema(tmp_path: Path):
    cfg = _config(tmp_path)
    store = ContentStore(cfg.context_repo)
    store.save_schema("", {"type": "legal-and-compliance", "criticality": "controlled"}, "admin")
    service = ContextService(cfg)

    package = service.assemble_context_package_v1(
        task="ad copy",
        scope_id=None,
        requests=[{"type": "legal-and-compliance", "query": "required disclaimer"}],
    )

    assert package["blocked"] is True
    assert package["results"][0]["resolved_criticality"] == "controlled"
    assert package["results"][0]["okf_records"] == []
    assert package["results"][0]["collection_results"] == []
    assert package["results"][0]["missing"][0]["blocks_workflow"] is True


def test_hybrid_context_searches_only_collections_named_by_okf_sources(tmp_path: Path):
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
    collections.add_document_text("sales-calls", "call.txt", "renewal risk and pipeline quality came up repeatedly")
    collections.add_document_text("excluded", "excluded.txt", "renewal risk should not appear from this collection")
    service = ContextService(cfg)

    package = service.assemble_context_package_v1(
        task="campaign brief",
        scope_id=None,
        requests=[{"type": "audience-profile", "query": "renewal risk"}],
    )

    result = package["results"][0]
    assert package["blocked"] is False
    assert [record["title"] for record in result["okf_records"]] == ["Sales leaders"]
    assert {item["citation"]["collection_id"] for item in result["collection_results"]} == {"sales-calls"}
    assert result["collection_results"][0]["citation"]["source_title"] == "call.txt"
    assert "content_hash" in result["collection_results"][0]["citation"]


def test_controlled_context_never_searches_collections(tmp_path: Path):
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

    package = service.assemble_context_package_v1(
        task="ad copy",
        scope_id=None,
        requests=[{"type": "legal-and-compliance", "query": "renewal risk"}],
    )

    result = package["results"][0]
    assert package["blocked"] is False
    assert result["resolved_criticality"] == "controlled"
    assert result["okf_records"]
    assert result["collection_results"] == []
    assert result["suggested_sources"] == []


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


def test_mcp_suggested_sources_are_filtered_by_rbac(tmp_path: Path):
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

    package = service.assemble_context_package_v1(
        task="campaign brief",
        scope_id=None,
        requests=[{"type": "audience-profile"}],
        user={"username": "viewer", "role": "viewer"},
    )

    result = package["results"][0]
    assert result["suggested_sources"] == [{"kind": "mcp", "value": "public-research"}]
    assert result["access_issues"] == [{"kind": "mcp", "value": "sales-calls", "reason": "insufficient role"}]


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
