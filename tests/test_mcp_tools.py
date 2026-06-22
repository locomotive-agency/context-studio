from __future__ import annotations

from pathlib import Path

import pytest

from context_system import mcp_server
from context_system.cms import ContentStore
from context_system.config import Config
from context_system.service import ContextService
from context_system.request_context import clear_request_user, set_request_user


def _config(tmp_path: Path, **overrides) -> Config:
    return Config(
        context_repository_path=str(tmp_path / "context_repo"),
        audit_path=str(tmp_path / "audit.sqlite"),
        users_path=str(tmp_path / "users.sqlite"),
        collections_root_path=str(tmp_path / "collections"),
        collections_db_path=str(tmp_path / "collections.sqlite"),
        **overrides,
    )


def _service_with_mcp_source(tmp_path: Path, **config_overrides) -> ContextService:
    cfg = _config(tmp_path, **config_overrides)
    cfg.mcp_servers = [
        {"id": "admin-source", "roles": ["admin"]},
        {"id": "public-source", "roles": ["viewer", "editor", "admin"]},
    ]
    store = ContentStore(cfg.context_repo)
    store.save_document(
        "audience/sales-leaders.md",
        {
            "type": "audience-profile",
            "title": "Sales leaders",
            "criticality": "hybrid",
            "status": "approved",
            "supporting_sources": {"mcp": ["admin-source", "public-source"]},
        },
        "Sales leaders context.",
        "admin",
    )
    return ContextService(cfg)


def test_mcp_context_package_requires_user_or_explicit_service_account(tmp_path: Path, monkeypatch):
    service = _service_with_mcp_source(tmp_path)
    monkeypatch.setattr(mcp_server, "service", service)
    clear_request_user()

    with pytest.raises(PermissionError, match="authenticated MCP user"):
        mcp_server.list_context_documents(type="audience-profile")


def test_mcp_context_package_uses_request_user_for_source_filtering(tmp_path: Path, monkeypatch):
    service = _service_with_mcp_source(tmp_path)
    monkeypatch.setattr(mcp_server, "service", service)
    set_request_user({"username": "viewer", "role": "viewer"})

    try:
        documents = mcp_server.list_context_documents(type="audience-profile")
    finally:
        clear_request_user()

    assert documents[0]["title"] == "Sales leaders"
    assert documents[0]["supporting_sources"]["mcp"] == ["admin-source", "public-source"]
    assert "body" not in documents[0]


def test_mcp_context_package_uses_explicit_service_account_role(tmp_path: Path, monkeypatch):
    service = _service_with_mcp_source(tmp_path, mcp_service_account_role="viewer")
    monkeypatch.setattr(mcp_server, "service", service)
    clear_request_user()

    documents = mcp_server.list_context_documents(type="audience-profile")

    assert documents[0]["title"] == "Sales leaders"
    assert "body" not in documents[0]


def test_mcp_tools_expose_context_contract_and_no_legacy_package_tools():
    for name in [
        "list_context_scopes",
        "list_context_types",
        "list_context_folders",
        "read_context_index",
        "read_context_log",
        "list_context_documents",
        "read_context_document",
        "search_collection",
        "read_collection_source",
        "validate_context",
    ]:
        assert hasattr(mcp_server, name)

    assert not hasattr(mcp_server, "get_construct")
    assert not hasattr(mcp_server, "assemble_context_package")
    assert not hasattr(mcp_server, "list_okf_bundle")
    assert not hasattr(mcp_server, "read_okf_document")
    assert not hasattr(mcp_server, "read_okf_index")
    assert not hasattr(mcp_server, "read_okf_log")
    assert not hasattr(mcp_server, "list_okf_types")
    assert not hasattr(mcp_server, "list_okf_scopes")
    assert not hasattr(mcp_server, "validate_context_bundle")


def test_mcp_tools_do_not_expose_global_collection_listing():
    assert not hasattr(mcp_server, "search_context")
    assert not hasattr(mcp_server, "list_collections")
    assert not hasattr(mcp_server, "list_collection_documents")
    assert not hasattr(mcp_server, "search_collections")


def test_list_context_documents_is_metadata_only_and_defaults_to_100(tmp_path: Path):
    cfg = _config(tmp_path, mcp_service_account_role="viewer")
    store = ContentStore(cfg.context_repo)
    for index in range(105):
        store.save_document(
            f"proof/doc-{index:03d}.md",
            {
                "type": "proof-points",
                "title": f"Proof {index:03d}",
                "status": "approved",
                "supporting_sources": {"collections": ["sales-calls"]},
            },
            f"Body {index:03d}.",
            "admin",
        )
    service = ContextService(cfg)

    documents = service.list_context_documents(type="proof-points")

    assert len(documents) == 100
    assert documents[0]["title"] == "Proof 000"
    assert documents[0]["path"] == "proof/doc-000.md"
    assert documents[0]["supporting_sources"]["collections"] == ["sales-calls"]
    assert "body" not in documents[0]


def test_read_context_document_returns_body_after_scope_check(tmp_path: Path):
    cfg = _config(tmp_path, mcp_service_account_role="viewer")
    store = ContentStore(cfg.context_repo)
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "product-data", "name": "Data", "level": "product", "parent_id": "company"}, "admin")
    store.save_document(
        "products/data.md",
        {
            "type": "product-and-offering",
            "title": "Data",
            "scope_id": "product-data",
            "status": "approved",
        },
        "Full Data product context.",
        "admin",
    )
    service = ContextService(cfg)

    document = service.read_context_document("products/data.md", scope_id="product-data")

    assert document["body"].strip() == "Full Data product context."
    assert document["path"] == "products/data.md"


def test_list_context_folders_can_filter_by_type_and_scope(tmp_path: Path):
    cfg = _config(tmp_path, mcp_service_account_role="viewer")
    store = ContentStore(cfg.context_repo)
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "product-data", "name": "Data", "level": "product", "parent_id": "company"}, "admin")
    store.save_document(
        "competitors/sub-products/apollo-b2b-data.md",
        {
            "type": "competitive-landscape",
            "title": "Apollo B2B Data",
            "scope_id": "product-data",
            "status": "approved",
        },
        "Apollo context.",
        "admin",
    )
    store.save_document(
        "products/data.md",
        {"type": "product-and-offering", "title": "Data", "scope_id": "product-data", "status": "approved"},
        "Data product context.",
        "admin",
    )
    service = ContextService(cfg)

    folders = service.list_context_folders(type="competitive-landscape", scope_id="product-data")

    assert [folder["path"] for folder in folders] == ["competitors", "competitors/sub-products"]


def test_collection_search_defaults_to_10_and_source_read_returns_logical_path(tmp_path: Path):
    cfg = _config(tmp_path, mcp_service_account_role="viewer")
    collections = ContextService(cfg).collections
    collections.create_collection("sales-calls", "Sales Calls")
    source = collections.add_document_text("sales-calls", "call.txt", "renewal risk\n\npipeline quality")
    service = ContextService(cfg)

    results = service.search_collection("sales-calls", "renewal")
    document = service.read_collection_source("sales-calls", results[0]["source_id"])

    assert len(results) <= 10
    assert results[0]["collection_id"] == "sales-calls"
    assert results[0]["source_id"] == source["id"]
    assert "snippet" in results[0]
    assert document["id"] == source["id"]
    assert document["source_path"] == "sales-calls/sources/call.txt"
    assert document["text"].startswith("renewal risk")
