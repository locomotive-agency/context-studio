from __future__ import annotations

import base64
from pathlib import Path

from fastapi import HTTPException
from fastapi.testclient import TestClient

from context_system import app as app_module
from context_system.auth import create_token
from context_system.cms import ContentStore
from context_system.config import Config
from context_system.service import ContextService


def _headers(role: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_token(role, role)}"}


def _temp_service(tmp_path: Path) -> tuple[Config, ContentStore, ContextService]:
    cfg = Config(
        context_repository_path=str(tmp_path / "context_repo"),
        audit_path=str(tmp_path / "audit.sqlite"),
        users_path=str(tmp_path / "users.sqlite"),
        collections_root_path=str(tmp_path / "collections"),
        collections_db_path=str(tmp_path / "collections.sqlite"),
    )
    store = ContentStore(cfg.context_repo)
    service = ContextService(cfg)
    return cfg, store, service


def test_context_and_semantic_routes_require_login() -> None:
    with TestClient(app_module.app) as client:
        responses = [
            client.get("/api/stats"),
            client.post("/api/mcp-tools/list_context_documents", json={"type": "brand-messaging"}),
            client.post("/mcp/"),
        ]

    assert {response.status_code for response in responses} == {401}


def test_document_semantic_search_route_is_removed() -> None:
    client = TestClient(app_module.app)

    response = client.get(
        "/api/search",
        headers=_headers("viewer"),
        params={"query": "brand"},
    )

    assert response.status_code == 404


def test_viewer_can_request_context_but_cannot_write() -> None:
    client = TestClient(app_module.app)

    read = client.post(
        "/api/mcp-tools/list_context_documents",
        headers=_headers("viewer"),
        json={"type": "brand-messaging"},
    )
    write = client.put(
        "/api/documents/viewer-test.md",
        headers=_headers("viewer"),
        json={"frontmatter": {"type": "test", "title": "Test"}, "body": "Body"},
    )

    assert read.status_code == 200
    assert write.status_code == 403


def test_legacy_context_package_routes_are_removed() -> None:
    client = TestClient(app_module.app)

    first = client.post(
        "/api/context-package",
        headers=_headers("viewer"),
        json={"task": "brand", "requests": [{"type": "brand-messaging"}]},
    )
    second = client.post(
        "/api/assemble_context_package",
        headers=_headers("viewer"),
        json={"task": "brand", "constructs": ["brand-messaging"]},
    )

    assert first.status_code == 404
    assert second.status_code == 404


def test_admin_can_edit_folder_metadata_and_import_okf_folder(tmp_path: Path, monkeypatch) -> None:
    _cfg, store, service = _temp_service(tmp_path)
    source = tmp_path / "source"
    source.mkdir()
    (source / "example.md").write_text("---\ntype: test\ntitle: Test\nstatus: approved\n---\n\nBody\n", encoding="utf-8")
    monkeypatch.setattr(app_module, "content", store)
    monkeypatch.setattr(app_module, "service", service)
    client = TestClient(app_module.app)

    schema = client.put(
        "/api/schemas",
        headers=_headers("admin"),
        json={"path": "", "schema": {"type": "test", "criticality": "flexible"}},
    )
    imported = client.post(
        "/api/imports/okf-folder/apply",
        headers=_headers("admin"),
        json={"source_folder": str(source)},
    )

    assert schema.status_code == 200
    assert imported.status_code == 200
    assert (store.repository / "example.md").is_file()


def test_admin_can_import_uploaded_okf_folder(tmp_path: Path, monkeypatch) -> None:
    _cfg, store, service = _temp_service(tmp_path)
    monkeypatch.setattr(app_module, "content", store)
    monkeypatch.setattr(app_module, "service", service)
    client = TestClient(app_module.app)
    payload = {
        "folder_name": "upload-source",
        "files": [
            {
                "path": "products/example.md",
                "content_base64": base64.b64encode(
                    b"---\ntype: test\ntitle: Test\nstatus: approved\n---\n\nBody\n"
                ).decode("ascii"),
            }
        ],
    }

    scanned = client.post(
        "/api/imports/okf-folder/scan-upload",
        headers=_headers("admin"),
        json=payload,
    )
    imported = client.post(
        "/api/imports/okf-folder/apply-upload",
        headers=_headers("admin"),
        json=payload,
    )

    assert scanned.status_code == 200
    assert scanned.json()["files"] == [{"path": "products/example.md", "kind": "markdown"}]
    assert imported.status_code == 200
    assert imported.json()["imported_files"] == ["products/example.md"]
    assert (store.repository / "products/example.md").read_text(encoding="utf-8").endswith("Body\n")


def test_uploaded_okf_import_rejects_paths_outside_selected_folder(tmp_path: Path, monkeypatch) -> None:
    _cfg, store, service = _temp_service(tmp_path)
    monkeypatch.setattr(app_module, "content", store)
    monkeypatch.setattr(app_module, "service", service)
    client = TestClient(app_module.app)

    response = client.post(
        "/api/imports/okf-folder/scan-upload",
        headers=_headers("admin"),
        json={
            "folder_name": "upload-source",
            "files": [{"path": "/server/path/example.md", "content": "Body"}],
        },
    )

    assert response.status_code == 400
    assert "relative" in response.json()["detail"]
    assert not (store.repository / "server/path/example.md").exists()


def test_editor_cannot_edit_schema_or_import_okf_folder(tmp_path: Path, monkeypatch) -> None:
    _cfg, store, service = _temp_service(tmp_path)
    source = tmp_path / "source"
    source.mkdir()
    (source / "example.md").write_text("---\ntype: test\ntitle: Test\nstatus: approved\n---\n\nBody\n", encoding="utf-8")
    monkeypatch.setattr(app_module, "content", store)
    monkeypatch.setattr(app_module, "service", service)
    client = TestClient(app_module.app)

    schema = client.put(
        "/api/schemas",
        headers=_headers("editor"),
        json={"path": "", "schema": {"type": "test", "criticality": "flexible"}},
    )
    scanned = client.post(
        "/api/imports/okf-folder/scan",
        headers=_headers("editor"),
        json={"source_folder": str(source)},
    )
    imported = client.post(
        "/api/imports/okf-folder/apply",
        headers=_headers("editor"),
        json={"source_folder": str(source)},
    )
    uploaded = client.post(
        "/api/imports/okf-folder/apply-upload",
        headers=_headers("editor"),
        json={"folder_name": "source", "files": [{"path": "example.md", "content": "Body"}]},
    )

    assert schema.status_code == 403
    assert scanned.status_code == 403
    assert imported.status_code == 403
    assert uploaded.status_code == 403
    assert not (store.repository / "example.md").exists()


def test_editor_can_upload_text_collection_document(tmp_path: Path, monkeypatch) -> None:
    _cfg, store, service = _temp_service(tmp_path)
    monkeypatch.setattr(app_module, "content", store)
    monkeypatch.setattr(app_module, "service", service)
    client = TestClient(app_module.app)

    collection = client.post(
        "/api/collections",
        headers=_headers("editor"),
        json={"id": "sales-calls", "name": "Sales Calls"},
    )
    uploaded = client.post(
        "/api/collections/sales-calls/documents",
        headers=_headers("editor"),
        json={"filename": "call.md", "content": "renewal risk and approved truth came up repeatedly"},
    )
    malformed = client.post(
        "/api/collections/sales-calls/documents",
        headers=_headers("editor"),
        json={"filename": "bad.md", "content": {"value": "not a string"}},
    )

    assert collection.status_code == 200
    assert uploaded.status_code == 200
    assert uploaded.json()["index_status"] == "indexed"
    assert malformed.status_code == 400
    assert malformed.json()["detail"] == "content must be a string"


def test_editor_can_move_documents_and_folders(tmp_path: Path, monkeypatch) -> None:
    _cfg, store, service = _temp_service(tmp_path)
    store.create_folder("archive", "admin")
    store.create_folder("products", "admin")
    store.save_document("example.md", {"type": "Reference", "title": "Example"}, "Body", "admin")
    store.save_document("products/product.md", {"type": "Reference", "title": "Product"}, "Body", "admin")
    monkeypatch.setattr(app_module, "content", store)
    monkeypatch.setattr(app_module, "service", service)
    client = TestClient(app_module.app)

    moved_document = client.post(
        "/api/documents/move",
        headers=_headers("editor"),
        json={"path": "example.md", "target_folder": "products"},
    )
    moved_folder = client.post(
        "/api/folders/move",
        headers=_headers("editor"),
        json={"path": "products", "target_parent": "archive"},
    )

    assert moved_document.status_code == 200
    assert moved_document.json()["path"] == "products/example.md"
    assert moved_folder.status_code == 200
    assert moved_folder.json()["path"] == "archive/products"
    assert (store.repository / "archive/products/example.md").is_file()
    assert (store.repository / "archive/products/product.md").is_file()


def test_editor_cannot_manage_users_or_scopes() -> None:
    client = TestClient(app_module.app)

    user_response = client.post(
        "/api/users",
        headers=_headers("editor"),
        json={"username": "role-test", "password": "pw", "role": "viewer"},
    )
    scope_response = client.post(
        "/api/scopes",
        headers=_headers("editor"),
        json={"id": "role-test", "name": "Role Test", "level": "company"},
    )

    assert user_response.status_code == 403
    assert scope_response.status_code == 403


def test_github_editor_cannot_use_admin_write_paths(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module.github_auth,
        "refresh_user_permission",
        lambda user, users: {"username": "octocat", "role": "editor", "provider": "github", "permission": "write"},
    )

    try:
        app_module._prepare_write({"username": "octocat", "role": "editor", "provider": "github"}, ["admin"])
    except HTTPException as exc:
        assert exc.status_code == 403
    else:
        raise AssertionError("GitHub editor should not pass admin-only write paths")
