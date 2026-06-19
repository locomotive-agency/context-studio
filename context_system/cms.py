from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .git_store import GitStore
from .okf import (
    RESERVED_DOCUMENTS,
    SCHEMA_FILE,
    load_effective_schema,
    parse_document,
    render_document,
    validate_frontmatter,
    validate_relative_path,
)
from .models import ScopeNode

SCOPES_FILE = "_scopes.yaml"


class ContentStore:
    def __init__(self, repository: Path):
        self.repository = repository
        self.git = GitStore(repository)

    def list_documents(self) -> list[dict[str, Any]]:
        documents = []
        paths = sorted([*self.repository.rglob("*.md"), *self.repository.rglob("*.json")])
        for path in paths:
            relative = path.relative_to(self.repository).as_posix()
            if ".git" in path.parts or path.name in RESERVED_DOCUMENTS:
                continue
            documents.append(self.read_document(relative, include_body=False))
        return documents

    def read_document(self, relative_path: str, include_body: bool = True) -> dict[str, Any]:
        relative_path = validate_relative_path(relative_path)
        if Path(relative_path).suffix.lower() not in {".md", ".json"}:
            raise ValueError("document path must end in .md or .json")
        path = self.repository / relative_path
        if not path.is_file():
            raise FileNotFoundError(relative_path)
        if path.suffix.lower() == ".json":
            raw = path.read_text(encoding="utf-8")
            try:
                json.loads(raw)
                validation_data = {"valid": True, "errors": []}
            except json.JSONDecodeError as exc:
                validation_data = {"valid": False, "errors": [f"invalid JSON: {exc.msg} at line {exc.lineno}"]}
            return {"path": relative_path, "name": path.stem, "folder": "" if path.parent == self.repository else path.parent.relative_to(self.repository).as_posix(), "format": "json", "frontmatter": {}, "effective_frontmatter": {}, "body": raw if include_body else "", "validation": validation_data}
        try:
            parsed = parse_document(path.read_text(encoding="utf-8"))
            schema = load_effective_schema(self.repository, relative_path)
            effective = schema | parsed.frontmatter
            validation = validate_frontmatter(parsed.frontmatter)
            frontmatter = parsed.frontmatter
            body = parsed.body if include_body else ""
        except ValueError as exc:
            schema, effective, frontmatter, body = {}, {}, {}, ""
            validation = {"valid": False, "errors": [str(exc)]}
        validation_data = validation.model_dump() if hasattr(validation, "model_dump") else validation
        return {
            "path": relative_path,
            "format": "markdown",
            "name": path.stem,
            "folder": "" if Path(relative_path).parent == Path(".") else Path(relative_path).parent.as_posix(),
            "frontmatter": frontmatter,
            "effective_frontmatter": effective,
            "body": body,
            "validation": validation_data,
        }

    def save_document(self, relative_path: str, frontmatter: dict[str, Any], body: str, author: str) -> dict[str, Any]:
        relative_path = validate_relative_path(relative_path)
        suffix = Path(relative_path).suffix.lower()
        if suffix not in {".md", ".json"}:
            raise ValueError("document path must end in .md or .json")
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if suffix == ".json":
            try:
                json.loads(body)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON: {exc.msg} at line {exc.lineno}") from exc
            path.write_text(body.rstrip() + "\n", encoding="utf-8")
            action = "Update" if self.git.history(relative_path, limit=1) else "Create"
            self.git.commit([relative_path], f"{action} {relative_path}", author)
            return self.read_document(relative_path)
        if Path(relative_path).name in RESERVED_DOCUMENTS:
            raise ValueError(f"{Path(relative_path).name} is reserved by OKF")
        validation = validate_frontmatter(frontmatter)
        if not validation.valid:
            raise ValueError("; ".join(validation.errors))
        path.write_text(render_document(frontmatter, body), encoding="utf-8")
        action = "Update" if self.git.history(relative_path, limit=1) else "Create"
        self.git.commit([relative_path], f"{action} {relative_path}", author)
        return self.read_document(relative_path)

    def restore_document(self, relative_path: str, commit: str, author: str) -> dict[str, Any]:
        relative_path = validate_relative_path(relative_path)
        suffix = Path(relative_path).suffix.lower()
        if suffix not in {".md", ".json"}:
            raise ValueError("document path must end in .md or .json")
        raw = self.git.file_at_revision(commit, relative_path)
        if suffix == ".json":
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"historical revision contains invalid JSON: {exc.msg}") from exc
        else:
            parsed = parse_document(raw)
            validation = validate_frontmatter(parsed.frontmatter)
            if not validation.valid:
                raise ValueError("historical revision is not valid OKF: " + "; ".join(validation.errors))
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(raw if raw.endswith("\n") else raw + "\n", encoding="utf-8")
        restored_commit = self.git.commit([relative_path], f"Restore {relative_path} to {commit[:7]}", author)
        return {"commit": restored_commit, "document": self.read_document(relative_path)}

    def create_folder(self, relative_path: str, author: str) -> dict[str, str]:
        relative_path = validate_relative_path(relative_path)
        schema_path = f"{relative_path}/{SCHEMA_FILE}"
        path = self.repository / schema_path
        if path.exists():
            raise FileExistsError(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
        self.git.commit([schema_path], f"Create folder {relative_path}", author)
        return {"path": relative_path}

    def list_folders(self) -> list[dict[str, Any]]:
        folders = {""}
        for document in self.list_documents():
            parent = Path(document["path"]).parent
            while str(parent) != ".":
                folders.add(parent.as_posix())
                parent = parent.parent
        for schema in self.repository.rglob(SCHEMA_FILE):
            folders.add(schema.parent.relative_to(self.repository).as_posix().replace(".", ""))
        return [self.read_schema(folder) for folder in sorted(folders)]

    def read_schema(self, folder: str) -> dict[str, Any]:
        clean = validate_relative_path(folder) if folder else ""
        path = self.repository / clean / SCHEMA_FILE
        schema = yaml.safe_load(path.read_text(encoding="utf-8")) or {} if path.exists() else {}
        return {"path": clean, "schema": schema}

    def save_schema(self, folder: str, schema: dict[str, Any], author: str) -> dict[str, Any]:
        clean = validate_relative_path(folder) if folder else ""
        path = self.repository / clean / SCHEMA_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(schema, sort_keys=False), encoding="utf-8")
        relative = path.relative_to(self.repository).as_posix()
        self.git.commit([relative], f"Update schema for {clean or 'root'}", author)
        return self.read_schema(clean)

    def validation_report(self) -> dict[str, Any]:
        documents = self.list_documents()
        invalid = [document for document in documents if not document["validation"]["valid"]]
        return {"valid": not invalid, "total": len(documents), "invalid": len(invalid), "documents": invalid}

    def list_scopes(self) -> list[dict[str, Any]]:
        path = self.repository / SCOPES_FILE
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {} if path.exists() else {}
        nodes = [ScopeNode.model_validate(item) for item in data.get("scopes", [])]
        return [node.model_dump() for node in nodes]

    def save_scope(self, data: dict[str, Any], author: str, existing_id: str | None = None) -> dict[str, Any]:
        scopes = self.list_scopes()
        by_id = {item["id"]: item for item in scopes}
        payload = dict(data)
        if "order" not in payload:
            if existing_id and existing_id in by_id:
                payload["order"] = by_id[existing_id].get("order", 0)
            else:
                parent_id = payload.get("parent_id")
                sibling_orders = [item.get("order", 0) for item in scopes if item.get("parent_id") == parent_id]
                payload["order"] = max(sibling_orders, default=-1) + 1
        node = ScopeNode.model_validate(payload)
        if existing_id and existing_id not in by_id:
            raise ValueError("scope not found")
        if not existing_id and node.id in by_id:
            raise ValueError("scope id already exists")
        if existing_id and node.id != existing_id:
            raise ValueError("scope id cannot be changed")
        if node.parent_id and node.parent_id not in by_id:
            raise ValueError("parent scope not found")
        if node.parent_id == node.id:
            raise ValueError("scope cannot be its own parent")
        ancestor = node.parent_id
        while ancestor:
            if ancestor == node.id:
                raise ValueError("scope hierarchy cannot contain a cycle")
            ancestor = by_id.get(ancestor, {}).get("parent_id")
        if existing_id:
            scopes = [node.model_dump() if item["id"] == existing_id else item for item in scopes]
            action = "Update"
        else:
            scopes.append(node.model_dump())
            action = "Create"
        self._write_scopes(scopes)
        self.git.commit([SCOPES_FILE], f"{action} scope {node.id}", author)
        return node.model_dump()

    def reorder_scopes(self, parent_id: str | None, ordered_ids: list[str], author: str) -> list[dict[str, Any]]:
        scopes = self.list_scopes()
        siblings = [item for item in scopes if item.get("parent_id") == parent_id]
        if len(ordered_ids) != len(set(ordered_ids)) or set(ordered_ids) != {item["id"] for item in siblings}:
            raise ValueError("ordered_ids must contain every sibling scope exactly once")
        order_by_id = {scope_id: index for index, scope_id in enumerate(ordered_ids)}
        updated = [item | {"order": order_by_id[item["id"]]} if item["id"] in order_by_id else item for item in scopes]
        self._write_scopes(updated)
        self.git.commit([SCOPES_FILE], f"Reorder scopes under {parent_id or 'root'}", author)
        return updated

    def move_scope(self, scope_id: str, parent_id: str | None, index: int, author: str) -> list[dict[str, Any]]:
        scopes = self.list_scopes()
        by_id = {item["id"]: item for item in scopes}
        if scope_id not in by_id:
            raise ValueError("scope not found")
        if parent_id and parent_id not in by_id:
            raise ValueError("parent scope not found")
        if parent_id == scope_id:
            raise ValueError("scope cannot be its own parent")
        ancestor = parent_id
        while ancestor:
            if ancestor == scope_id:
                raise ValueError("scope cannot be moved under one of its descendants")
            ancestor = by_id[ancestor].get("parent_id")

        source = by_id[scope_id]
        old_parent_id = source.get("parent_id")
        new_siblings = sorted(
            [item for item in scopes if item.get("parent_id") == parent_id and item["id"] != scope_id],
            key=lambda item: (item.get("order", 0), item["name"]),
        )
        target_index = max(0, min(index, len(new_siblings)))
        moved = source | {"parent_id": parent_id}
        new_siblings.insert(target_index, moved)
        updates = {item["id"]: item | {"order": order} for order, item in enumerate(new_siblings)}

        if old_parent_id != parent_id:
            old_siblings = sorted(
                [item for item in scopes if item.get("parent_id") == old_parent_id and item["id"] != scope_id],
                key=lambda item: (item.get("order", 0), item["name"]),
            )
            updates.update({item["id"]: item | {"order": order} for order, item in enumerate(old_siblings)})

        updated = [updates.get(item["id"], item) for item in scopes]
        self._write_scopes(updated)
        destination = parent_id or "root"
        self.git.commit([SCOPES_FILE], f"Move scope {scope_id} under {destination}", author)
        return updated

    def delete_scope(self, scope_id: str, author: str) -> None:
        scopes = self.list_scopes()
        if not any(item["id"] == scope_id for item in scopes):
            raise ValueError("scope not found")
        if any(item.get("parent_id") == scope_id for item in scopes):
            raise ValueError("scope has child scopes")
        if any(document["effective_frontmatter"].get("scope_id") == scope_id for document in self.list_documents()):
            raise ValueError("scope is assigned to documents")
        self._write_scopes([item for item in scopes if item["id"] != scope_id])
        self.git.commit([SCOPES_FILE], f"Delete scope {scope_id}", author)

    def scope_ancestors(self, scope_id: str) -> list[str]:
        by_id = {item["id"]: item for item in self.list_scopes()}
        if scope_id not in by_id:
            raise ValueError("scope not found")
        chain = []
        current: str | None = scope_id
        while current:
            chain.append(current)
            current = by_id[current].get("parent_id")
        return list(reversed(chain))

    def _write_scopes(self, scopes: list[dict[str, Any]]) -> None:
        path = self.repository / SCOPES_FILE
        path.write_text(yaml.safe_dump({"scopes": scopes}, sort_keys=False), encoding="utf-8")
