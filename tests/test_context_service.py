from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from context_system import app as app_module
from context_system.auth import UserStore, create_token, github_role_for_permission, verify_token
from context_system.cms import ContentStore
from context_system.config import Config
from context_system.git_store import GitStore
from context_system.repository import ContextRepository
from context_system.service import ContextService


def test_list_context_documents_returns_metadata_for_controlled_records():
    service = ContextService(Config(context_repository_path="demo/context_repo"))
    records = service.list_context_documents(type="brand-messaging", limit=10)

    assert records
    assert all(record["criticality"] == "controlled" for record in records)
    assert all("body" not in record for record in records)


def test_document_semantic_search_route_is_removed():
    client = TestClient(app_module.app)
    response = client.get(
        "/api/search",
        headers={"Authorization": f"Bearer {create_token('viewer', 'viewer')}"},
        params={"query": "customer case study revenue operations"},
    )

    assert response.status_code == 404


def test_api_mcp_tool_dispatch_lists_context_documents():
    cfg = Config(context_repository_path="demo/context_repo")
    original_service = app_module.service
    app_module.service = ContextService(cfg)
    client = TestClient(app_module.app)
    response = client.post(
        "/api/mcp-tools/list_context_documents",
        headers={"Authorization": f"Bearer {create_token('viewer', 'viewer')}"},
        json={"type": "brand-messaging"},
    )
    app_module.service = original_service

    assert response.status_code == 200
    payload = response.json()
    assert payload["tool"] == "list_context_documents"
    assert payload["result"]
    assert "body" not in payload["result"][0]


def test_authenticated_records_list():
    original_content = app_module.content
    app_module.content = ContentStore(Config(context_repository_path="demo/context_repo").context_repo)
    client = TestClient(app_module.app)
    login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert login.status_code == 200

    response = client.get("/api/records")
    app_module.content = original_content
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

    service = ContextService(config)
    records = service.list_context_documents(type="business-goals")

    assert [record["title"] for record in records] == ["Current"]


def test_runtime_record_lookup_reuses_cached_documents(tmp_path: Path, monkeypatch):
    repository_path = tmp_path / "context"
    store = ContentStore(repository_path)
    store.save_document("goals.md", {"type": "business-goals", "title": "Goals"}, "Goals", "admin")
    store.save_document("brand.md", {"type": "brand-messaging", "title": "Brand"}, "Brand", "admin")
    config = Config(context_repository_path=str(repository_path), audit_path=str(tmp_path / "audit.sqlite"), users_path=str(tmp_path / "users.sqlite"))
    repository = ContextRepository(config)
    calls: list[tuple[str, bool]] = []
    original_read_document = repository.content.read_document

    def counted_read_document(relative_path: str, include_body: bool = True):
        calls.append((relative_path, include_body))
        return original_read_document(relative_path, include_body=include_body)

    monkeypatch.setattr(repository.content, "read_document", counted_read_document)

    assert [record.title for record in repository.runtime_records() if record.type == "business-goals"] == ["Goals"]
    first_lookup_calls = len(calls)
    assert [record.title for record in repository.runtime_records() if record.type == "brand-messaging"] == ["Brand"]

    assert len(calls) == first_lookup_calls


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


def test_document_can_be_moved_to_an_existing_folder(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.create_folder("products", "editor")
    store.save_document("example.md", {"type": "Reference", "title": "Example"}, "Body", "editor")

    moved = store.move_document("example.md", "products", "editor")

    assert moved["path"] == "products/example.md"
    assert (tmp_path / "context" / "products/example.md").is_file()
    assert not (tmp_path / "context" / "example.md").exists()


def test_folder_can_be_moved_under_another_folder(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.create_folder("archive", "editor")
    store.create_folder("products", "editor")
    store.save_schema("products", {"type": "Reference"}, "admin")
    store.save_document("products/example.md", {"title": "Example"}, "Body", "editor")

    moved = store.move_folder("products", "archive", "editor")

    assert moved["path"] == "archive/products"
    assert (tmp_path / "context" / "archive/products/example.md").is_file()
    assert (tmp_path / "context" / "archive/products/_schema.yaml").is_file()
    assert not (tmp_path / "context" / "products").exists()


def test_folder_cannot_be_moved_into_itself_or_descendant(tmp_path: Path):
    store = ContentStore(tmp_path / "context")
    store.create_folder("products", "editor")
    store.create_folder("products/enterprise", "editor")

    for destination in ["products", "products/enterprise"]:
        try:
            store.move_folder("products", destination, "editor")
        except ValueError as exc:
            assert "descendant" in str(exc) or "itself" in str(exc)
        else:
            raise AssertionError(f"moving products to {destination} should fail")


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

    service = ContextService(config)
    records = service.list_context_documents(type="product-and-offering", scope_id="product")

    assert [record["title"] for record in records] == ["Company offering", "Product offering"]


def test_document_listing_reuses_scope_metadata(tmp_path: Path, monkeypatch):
    repository_path = tmp_path / "context"
    store = ContentStore(repository_path)
    store.save_scope({"id": "company", "name": "Company", "level": "company"}, "admin")
    for index in range(3):
        store.save_document(
            f"doc-{index}.md",
            {"type": "business-goals", "title": f"Doc {index}", "scope_id": "company"},
            "Body",
            "admin",
        )

    scope_reads = 0
    original_read_text = Path.read_text

    def counted_read_text(path: Path, *args, **kwargs):
        nonlocal scope_reads
        if path.name == "_scopes.yaml":
            scope_reads += 1
        return original_read_text(path, *args, **kwargs)

    store = ContentStore(repository_path)
    monkeypatch.setattr(Path, "read_text", counted_read_text)

    documents = store.list_documents()

    assert len(documents) == 3
    assert scope_reads == 1


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
