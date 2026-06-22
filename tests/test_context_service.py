from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from context_system.app import app
from context_system.auth import UserStore, create_token, github_role_for_permission, verify_token
from context_system.cms import ContentStore
from context_system.config import Config
from context_system.git_store import GitStore
from context_system.repository import ContextRepository
from context_system.service import ContextService


def test_assemble_package_returns_controlled_records():
    service = ContextService()
    package = service.assemble_construct_context_package(
        task="landing-page",
        constructs=["brand-messaging", "how-we-sound"],
        run_id="test-run",
    )

    assert not package.blocked
    assert len(package.records) >= 2
    assert any(record["criticality"] == "controlled" for record in package.records)


def test_search_no_longer_runs_over_okf_records():
    service = ContextService()
    results = service.search("customer case study revenue operations", constructs=["proof-points"], top_k=3)

    assert results == []


def test_api_assemble_contract_for_content_improve():
    client = TestClient(app)
    response = client.post(
        "/api/assemble_context_package",
        headers={"Authorization": f"Bearer {create_token('viewer', 'viewer')}"},
        json={"task": "brand_terms", "constructs": ["brand-messaging"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["task"] == "brand_terms"
    assert payload["blocked"] is False
    assert payload["records"]


def test_authenticated_records_list():
    client = TestClient(app)
    login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert login.status_code == 200

    response = client.get("/api/records")
    assert response.status_code == 200
    assert response.json()


def test_frontmatter_overrides_folder_schema(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.save_schema("", {"criticality": "hybrid", "type": "general"}, "admin")
    store.save_schema("brand", {"criticality": "controlled", "type": "brand-messaging"}, "admin")
    document = store.save_document(
        "brand/example.md",
        {"type": "proof-points", "title": "Example", "criticality": "flexible"},
        "# Example",
        "editor",
    )

    assert document["effective_frontmatter"]["type"] == "proof-points"
    assert document["effective_frontmatter"]["criticality"] == "flexible"
    assert store.git.history("brand/example.md")[0]["author"] == "editor"


def test_folder_scope_and_dates_are_inherited_and_document_scope_can_override(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "campaign", "name": "Campaign", "level": "campaign", "parent_id": "company"}, "admin")
    store.save_schema(
        "campaigns",
        {
            "type": "business-goals",
            "scope_id": "campaign",
            "durability": "time_bound",
            "valid_until": "2026-06-30",
        },
        "admin",
    )

    inherited = store.save_document("campaigns/brief.md", {"type": "Brief", "title": "Brief"}, "Campaign", "editor")
    overridden = store.save_document("campaigns/company.md", {"type": "Brief", "title": "Company", "scope_id": "company"}, "Company", "editor")

    assert inherited["effective_frontmatter"]["scope_id"] == "campaign"
    assert inherited["effective_frontmatter"]["valid_until"] == "2026-06-30"
    assert overridden["effective_frontmatter"]["scope_id"] == "company"


def test_time_bound_schema_requires_good_until_date(tmp_path: Path):
    store = ContentStore(tmp_path / "context")

    try:
        store.save_schema("campaigns", {"durability": "time_bound"}, "admin")
    except ValueError as exc:
        assert "valid_until" in str(exc)
    else:
        raise AssertionError("time-bound schema should require a good-until date")


def test_expired_context_is_excluded_from_retrieval(tmp_path: Path):
    repository_path = tmp_path / "context"
    store = ContentStore(repository_path)
    today = date.today()
    base = {"type": "business-goals", "status": "approved", "durability": "time_bound"}
    store.save_document("expired.md", base | {"title": "Expired", "valid_until": today - timedelta(days=1)}, "Expired", "admin")
    store.save_document("current.md", base | {"title": "Current", "valid_until": today + timedelta(days=1)}, "Current", "admin")
    config = Config(context_repository_path=str(repository_path), audit_path=str(tmp_path / "audit.sqlite"), users_path=str(tmp_path / "users.sqlite"))

    records = ContextRepository(config).get_construct("business-goals")

    assert [record.title for record in records] == ["Current"]


def test_invalid_okf_document_is_visible_in_report(tmp_path: Path):
    repository = tmp_path / "context"
    repository.mkdir()
    (repository / "broken.md").write_text("# Missing frontmatter\n", encoding="utf-8")
    store = ContentStore(repository)

    report = store.validation_report()

    assert report["invalid"] == 1
    assert report["documents"][0]["path"] == "broken.md"


def test_json_document_can_be_read_and_saved(tmp_path: Path):
    store = ContentStore(tmp_path / "context")

    document = store.save_document("sources/example.json", {}, '{"name": "Example"}', "admin")

    assert document["format"] == "json"
    assert document["validation"]["valid"]
    assert '"Example"' in document["body"]


def test_document_can_be_restored_as_a_new_revision(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    frontmatter = {"type": "Reference", "title": "Example"}
    store.save_document("example.md", frontmatter, "First version", "editor")
    first_revision = store.git.history("example.md")[0]["hash"]
    store.save_document("example.md", frontmatter, "Second version", "editor")
    second_revision = store.git.history("example.md")[0]["hash"]

    diff = store.git.diff(second_revision, "example.md")
    restored = store.restore_document("example.md", first_revision, "admin")

    assert "-First version" in diff
    assert "+Second version" in diff
    assert restored["document"]["body"].strip() == "First version"
    assert store.git.history("example.md")[0]["subject"].startswith("Restore example.md")


def test_document_can_be_deleted_as_a_git_revision(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.save_document("example.md", {"type": "Reference", "title": "Example"}, "Body", "editor")

    store.delete_document("example.md", "editor")

    assert not (tmp_path / "context" / "example.md").exists()
    assert store.git.history()[0]["subject"] == "Delete example.md"


def test_empty_folder_can_be_deleted_but_folder_with_documents_is_protected(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.create_folder("empty", "editor")
    store.create_folder("occupied", "editor")
    store.save_document("occupied/example.md", {"type": "Reference", "title": "Example"}, "Body", "editor")

    store.delete_folder("empty", "editor")

    assert not (tmp_path / "context" / "empty").exists()
    try:
        store.delete_folder("occupied", "editor")
    except ValueError as exc:
        assert "contains documents" in str(exc)
    else:
        raise AssertionError("folder with documents should not be deleted")


def test_user_store_updates_password_role_and_removes_user(tmp_path: Path):
    users = UserStore(tmp_path / "users.sqlite")

    assert users.update_user("editor", "admin", "new-password")
    assert users.get_user("editor")["role"] == "admin"
    assert users.delete_user("viewer")
    assert users.get_user("viewer") is None


def test_user_store_seeds_local_demo_users_from_config(tmp_path: Path):
    cfg = Config(
        users_path=str(tmp_path / "users.sqlite"),
        local_demo_users=[
            {"username": "owner", "password": "owner-password", "role": "admin"},
            {"username": "reviewer", "password": "reviewer-password", "role": "viewer"},
        ],
    )

    users = UserStore(config=cfg)

    assert users.get_user("owner")["role"] == "admin"
    assert users.get_user("reviewer")["role"] == "viewer"
    assert users.get_user("admin") is None


def test_user_store_keeps_at_least_one_admin(tmp_path: Path):
    users = UserStore(tmp_path / "users.sqlite")

    try:
        users.delete_user("admin")
    except ValueError as exc:
        assert "at least one admin" in str(exc)
    else:
        raise AssertionError("last admin removal should fail")


def test_github_permissions_map_to_local_roles():
    assert github_role_for_permission("admin") == "admin"
    assert github_role_for_permission("write") == "editor"
    assert github_role_for_permission("maintain") == "editor"
    assert github_role_for_permission("read") == "viewer"
    assert github_role_for_permission("triage") == "viewer"
    assert github_role_for_permission("none") is None


def test_runtime_records_do_not_expose_edit_roles(tmp_path: Path):
    repository_path = tmp_path / "context"
    store = ContentStore(repository_path)
    store.save_document(
        "example.md",
        {"type": "Reference", "title": "Example", "status": "approved"},
        "Body",
        "admin",
    )
    config = Config(context_repository_path=str(repository_path), audit_path=str(tmp_path / "audit.sqlite"), users_path=str(tmp_path / "users.sqlite"))

    record = ContextRepository(config).runtime_records()[0].model_dump()

    assert "edit_roles" not in record


def test_github_session_token_keeps_only_session_reference():
    token = create_token("octocat", "editor", "github", "session-123")
    payload = verify_token(token)

    assert payload == {"username": "octocat", "role": "editor", "provider": "github", "session_id": "session-123"}


def test_git_sync_and_push_skip_repositories_without_origin(tmp_path: Path):
    git = GitStore(tmp_path / "context")

    assert git.sync_with_remote() == {"synced": False, "reason": "no origin remote"}
    assert git.push_to_remote() == {"pushed": False, "reason": "no origin remote"}


def test_scope_hierarchy_prefers_most_specific_context(tmp_path: Path):
    repository_path = tmp_path / "context"
    store = ContentStore(repository_path)
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "product", "name": "Product", "level": "product", "parent_id": "company"}, "admin")
    base = {"type": "product-and-offering", "status": "approved", "criticality": "hybrid"}
    store.save_document("company.md", base | {"title": "Company offering", "scope_id": "company"}, "Company", "admin")
    store.save_document("product.md", base | {"title": "Product offering", "scope_id": "product"}, "Product", "admin")
    config = Config(context_repository_path=str(repository_path), audit_path=str(tmp_path / "audit.sqlite"), users_path=str(tmp_path / "users-2.sqlite"))

    records = ContextRepository(config).get_construct("product-and-offering", scope_id="product")

    assert [record.title for record in records] == ["Product offering"]


def test_scope_siblings_can_be_reordered(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "brand-a", "name": "Brand A", "level": "brand", "parent_id": "company"}, "admin")
    store.save_scope({"id": "brand-b", "name": "Brand B", "level": "brand", "parent_id": "company"}, "admin")

    store.reorder_scopes("company", ["brand-b", "brand-a"], "admin")

    scopes = {scope["id"]: scope for scope in store.list_scopes()}
    assert scopes["brand-b"]["order"] == 0
    assert scopes["brand-a"]["order"] == 1


def test_scope_can_be_moved_to_a_new_parent(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "brand-a", "name": "Brand A", "level": "brand", "parent_id": "company"}, "admin")
    store.save_scope({"id": "brand-b", "name": "Brand B", "level": "brand", "parent_id": "company"}, "admin")
    store.save_scope({"id": "product", "name": "Product", "level": "product", "parent_id": "brand-b"}, "admin")

    store.move_scope("product", "brand-a", 0, "admin")

    scopes = {scope["id"]: scope for scope in store.list_scopes()}
    assert scopes["product"]["parent_id"] == "brand-a"
    assert scopes["product"]["order"] == 0


def test_scope_cannot_be_moved_under_its_descendant(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "brand", "name": "Brand", "level": "brand", "parent_id": "company"}, "admin")

    try:
        store.move_scope("company", "brand", 0, "admin")
    except ValueError as exc:
        assert "descendants" in str(exc)
    else:
        raise AssertionError("cyclic scope move should fail")
