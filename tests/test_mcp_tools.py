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
        mcp_server.assemble_context_package(
            task="campaign brief",
            requests=[{"type": "audience-profile"}],
        )


def test_mcp_context_package_uses_request_user_for_source_filtering(tmp_path: Path, monkeypatch):
    service = _service_with_mcp_source(tmp_path)
    monkeypatch.setattr(mcp_server, "service", service)
    set_request_user({"username": "viewer", "role": "viewer"})

    try:
        package = mcp_server.assemble_context_package(
            task="campaign brief",
            requests=[{"type": "audience-profile"}],
        )
    finally:
        clear_request_user()

    result = package["results"][0]
    assert result["suggested_sources"] == [{"kind": "mcp", "value": "public-source"}]
    assert result["access_issues"] == [{"kind": "mcp", "value": "admin-source", "reason": "insufficient role"}]


def test_mcp_context_package_uses_explicit_service_account_role(tmp_path: Path, monkeypatch):
    service = _service_with_mcp_source(tmp_path, mcp_service_account_role="viewer")
    monkeypatch.setattr(mcp_server, "service", service)
    clear_request_user()

    package = mcp_server.assemble_context_package(
        task="campaign brief",
        requests=[{"type": "audience-profile"}],
    )

    result = package["results"][0]
    assert result["suggested_sources"] == [{"kind": "mcp", "value": "public-source"}]
    assert result["access_issues"] == [{"kind": "mcp", "value": "admin-source", "reason": "insufficient role"}]


def test_mcp_tools_do_not_expose_direct_collection_listing_or_search():
    assert not hasattr(mcp_server, "list_collections")
    assert not hasattr(mcp_server, "list_collection_documents")
    assert not hasattr(mcp_server, "search_collection")
    assert not hasattr(mcp_server, "search_collections")
