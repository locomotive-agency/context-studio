from __future__ import annotations

from pathlib import Path

from context_system.cms import ContentStore
from context_system.config import Config
from context_system.demo_workspace import initialize_demo_workspace
from context_system.service import ContextService


def test_initialize_demo_workspace_copies_seed_context_and_collections(tmp_path: Path):
    cfg = Config(
        context_repository_path=str(tmp_path / ".local" / "context_repo"),
        audit_path=str(tmp_path / ".local" / "var" / "audit.sqlite"),
        users_path=str(tmp_path / ".local" / "var" / "users.sqlite"),
        collections_root_path=str(tmp_path / ".local" / "var" / "collections"),
        collections_db_path=str(tmp_path / ".local" / "var" / "collections.sqlite"),
    )

    result = initialize_demo_workspace(cfg)

    assert result["copied_context_repo"] is True
    assert (cfg.context_repo / "brand" / "positioning.md").is_file()
    assert cfg.collections_db.is_file()
    assert result["baseline_commit"] != "uncommitted"
    assert result["collection"]["id"] == "enterprise-sales-conversations"
    assert result["collection"]["indexed_sources"] == 5

    store = ContentStore(cfg.context_repo)
    assert store.git.repository == cfg.context_repo
    assert (cfg.context_repo / ".git").is_dir()
    assert store.git.status() == []

    service = ContextService(cfg)
    records = service.list_context_documents(type="brand-messaging", scope_id="context-studio-brand")
    results = service.search_collection("enterprise-sales-conversations", "approved truth", limit=3)

    assert records[0]["title"] == "Context Studio Brand Positioning"
    assert results


def test_initialize_demo_workspace_preserves_existing_context_without_reset(tmp_path: Path):
    cfg = Config(
        context_repository_path=str(tmp_path / ".local" / "context_repo"),
        collections_root_path=str(tmp_path / ".local" / "var" / "collections"),
        collections_db_path=str(tmp_path / ".local" / "var" / "collections.sqlite"),
    )
    initialize_demo_workspace(cfg)
    marker = cfg.context_repo / "local-edit.md"
    marker.write_text("---\ntype: reference\ntitle: Local Edit\n---\n\nLocal", encoding="utf-8")

    result = initialize_demo_workspace(cfg)

    assert result["copied_context_repo"] is False
    assert marker.is_file()


def test_reset_demo_workspace_recreates_context(tmp_path: Path):
    cfg = Config(
        context_repository_path=str(tmp_path / ".local" / "context_repo"),
        audit_path=str(tmp_path / ".local" / "var" / "audit.sqlite"),
        users_path=str(tmp_path / ".local" / "var" / "users.sqlite"),
        collections_root_path=str(tmp_path / ".local" / "var" / "collections"),
        collections_db_path=str(tmp_path / ".local" / "var" / "collections.sqlite"),
    )
    initialize_demo_workspace(cfg)
    marker = cfg.context_repo / "local-edit.md"
    marker.write_text("---\ntype: reference\ntitle: Local Edit\n---\n\nLocal", encoding="utf-8")
    cfg.audit_db.parent.mkdir(parents=True, exist_ok=True)
    cfg.audit_db.write_text("audit", encoding="utf-8")
    cfg.users_db.write_text("users", encoding="utf-8")

    result = initialize_demo_workspace(cfg, reset=True)

    assert result["copied_context_repo"] is True
    assert not marker.exists()
    assert str(cfg.audit_db) in result["cleared_databases"]
    assert str(cfg.users_db) in result["cleared_databases"]
    assert not cfg.audit_db.exists()
    assert not cfg.users_db.exists()
