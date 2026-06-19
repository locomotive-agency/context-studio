from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from context_system.app import app
from context_system.auth import UserStore
from context_system.cms import ContentStore
from context_system.config import Config
from context_system.repository import ContextRepository
from context_system.service import ContextService


def test_assemble_package_returns_controlled_exact_language():
    service = ContextService()
    package = service.assemble_context_package(
        task="landing-page",
        constructs=["brand-messaging", "how-we-sound"],
        run_id="test-run",
    )

    assert not package.blocked
    assert len(package.records) >= 2
    assert "ctx.brand-messaging.terminology" in package.exact_language_map


def test_search_returns_hybrid_pointers_only():
    service = ContextService()
    results = service.search("customer case study revenue operations", constructs=["proof-points"], top_k=3)

    assert results
    assert all(result["construct"] == "proof-points" for result in results)


def test_api_assemble_contract_for_content_improve():
    client = TestClient(app)
    response = client.post(
        "/api/assemble_context_package",
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
    store.save_schema("", {"criticality": "hybrid", "construct": "general"}, "admin")
    store.save_schema("brand", {"criticality": "controlled", "construct": "brand"}, "admin")
    document = store.save_document(
        "brand/example.md",
        {"type": "Reference", "title": "Example", "criticality": "flexible"},
        "# Example",
        "editor",
    )

    assert document["effective_frontmatter"]["construct"] == "brand"
    assert document["effective_frontmatter"]["criticality"] == "flexible"
    assert store.git.history("brand/example.md")[0]["author"] == "editor"


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


def test_user_store_updates_password_role_and_removes_user(tmp_path: Path):
    users = UserStore(tmp_path / "users.sqlite")

    assert users.update_user("editor", "admin", "new-password")
    assert users.get_user("editor")["role"] == "admin"
    assert users.delete_user("viewer")
    assert users.get_user("viewer") is None


def test_user_store_keeps_at_least_one_admin(tmp_path: Path):
    users = UserStore(tmp_path / "users.sqlite")

    try:
        users.delete_user("admin")
    except ValueError as exc:
        assert "at least one admin" in str(exc)
    else:
        raise AssertionError("last admin removal should fail")


def test_scope_hierarchy_prefers_most_specific_context(tmp_path: Path):
    repository_path = tmp_path / "context"
    store = ContentStore(repository_path)
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    store.save_scope({"id": "product", "name": "Product", "level": "product", "parent_id": "company"}, "admin")
    base = {"type": "Reference", "construct": "product-offering", "owner_role": "editor", "status": "approved", "criticality": "hybrid"}
    store.save_document("company.md", base | {"title": "Company offering", "scope_id": "company"}, "Company", "admin")
    store.save_document("product.md", base | {"title": "Product offering", "scope_id": "product"}, "Product", "admin")
    config = Config(context_repository_path=str(repository_path), audit_path=str(tmp_path / "audit.sqlite"), users_path=str(tmp_path / "users-2.sqlite"))

    records = ContextRepository(config).get_construct("product-offering", scope_id="product")

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
