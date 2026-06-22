from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import yaml

from .git_store import GitStore
from .okf import (
    RESERVED_DOCUMENTS,
    SCHEMA_FILE,
    load_effective_schema,
    merge_metadata,
    parse_markdown_metadata,
    parse_document,
    render_document,
    validate_frontmatter,
    validate_governance,
    validate_relative_path,
)
from .models import ScopeNode

SCOPES_FILE = "_scopes.yaml"


class ContentStore:
    def __init__(self, repository: Path):
        self.repository = repository
        self.git = GitStore(repository)
        self._scopes_cache: tuple[int | None, list[dict[str, Any]]] | None = None

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
            return {"path": relative_path, "name": path.stem, "folder": "" if path.parent == self.repository else path.parent.relative_to(self.repository).as_posix(), "format": "json", "frontmatter": {}, "inherited_frontmatter": {}, "effective_frontmatter": {}, "body": raw if include_body else "", "validation": validation_data}
        try:
            parsed = parse_document(path.read_text(encoding="utf-8"))
            schema = load_effective_schema(self.repository, relative_path)
            effective = merge_metadata(schema, parsed.frontmatter)
            okf_validation = validate_frontmatter(effective)
            governance_errors = self._governance_errors(effective)
            validation = {"valid": okf_validation.valid and not governance_errors, "errors": okf_validation.errors + governance_errors}
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
            "inherited_frontmatter": schema,
            "effective_frontmatter": effective,
            "body": body,
            "validation": validation_data,
        }

    def list_okf_entries(self, folder: str | None = None) -> list[dict[str, Any]]:
        clean = validate_relative_path(folder or "") if folder else ""
        root = self.repository / clean
        if not root.exists():
            raise FileNotFoundError(clean)
        paths = sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)
        return [self.read_okf_entry(path.relative_to(self.repository).as_posix(), include_body=False) for path in paths]

    def read_okf_entry(self, relative_path: str, include_body: bool = True) -> dict[str, Any]:
        relative_path = validate_relative_path(relative_path, suffix=".md")
        path = self.repository / relative_path
        if not path.is_file():
            raise FileNotFoundError(relative_path)
        kind = self._okf_kind(path.name)
        if kind == "concept":
            raw = path.read_text(encoding="utf-8")
            entry = self.read_document(relative_path, include_body=include_body)
            try:
                metadata_body = parse_document(raw).body
            except ValueError:
                metadata_body = entry["body"]
            metadata = parse_markdown_metadata(metadata_body, relative_path)
            entry.update(
                {
                    "kind": kind,
                    "title": entry["effective_frontmatter"].get("title"),
                    "type": entry["effective_frontmatter"].get("type"),
                    "scope_id": entry["effective_frontmatter"].get("scope_id"),
                    "status": entry["effective_frontmatter"].get("status"),
                    "description": entry["effective_frontmatter"].get("description"),
                    "links": metadata.internal_links,
                    "external_links": metadata.external_links,
                    "citations": metadata.citations,
                    "headings": metadata.headings,
                    "content_hash": self._content_hash(relative_path),
                }
            )
            return entry
        raw = path.read_text(encoding="utf-8")
        body = raw if include_body else ""
        metadata = parse_markdown_metadata(raw, relative_path)
        return {
            "path": relative_path,
            "format": "markdown",
            "kind": kind,
            "name": path.stem,
            "folder": "" if Path(relative_path).parent == Path(".") else Path(relative_path).parent.as_posix(),
            "frontmatter": {},
            "inherited_frontmatter": {},
            "effective_frontmatter": {},
            "body": body,
            "validation": {"valid": True, "errors": []},
            "title": metadata.headings[0]["text"] if metadata.headings else path.stem,
            "type": None,
            "scope_id": None,
            "status": None,
            "description": None,
            "links": metadata.internal_links,
            "external_links": metadata.external_links,
            "citations": metadata.citations,
            "headings": metadata.headings,
            "content_hash": self._content_hash(relative_path),
        }

    def read_okf_index(self, folder: str | None = None) -> dict[str, Any]:
        path = Path(validate_relative_path(folder or "") if folder else "") / "index.md"
        return self.read_okf_entry(path.as_posix())

    def read_okf_log(self, folder: str | None = None) -> dict[str, Any]:
        path = Path(validate_relative_path(folder or "") if folder else "") / "log.md"
        return self.read_okf_entry(path.as_posix())

    @staticmethod
    def _okf_kind(name: str) -> str:
        if name == "index.md":
            return "index"
        if name == "log.md":
            return "log"
        return "concept"

    def _content_hash(self, relative_path: str) -> str:
        return __import__("hashlib").sha256((self.repository / relative_path).read_bytes()).hexdigest()[:16]

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
        effective = merge_metadata(load_effective_schema(self.repository, relative_path), frontmatter)
        validation = validate_frontmatter(effective)
        if not validation.valid:
            raise ValueError("; ".join(validation.errors))
        governance_errors = self._governance_errors(effective)
        if governance_errors:
            raise ValueError("; ".join(governance_errors))
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
            effective = merge_metadata(load_effective_schema(self.repository, relative_path), parsed.frontmatter)
            validation = validate_frontmatter(effective)
            if not validation.valid:
                raise ValueError("historical revision is not valid OKF: " + "; ".join(validation.errors))
            governance_errors = self._governance_errors(effective)
            if governance_errors:
                raise ValueError("historical revision has invalid governance: " + "; ".join(governance_errors))
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(raw if raw.endswith("\n") else raw + "\n", encoding="utf-8")
        restored_commit = self.git.commit([relative_path], f"Restore {relative_path} to {commit[:7]}", author)
        return {"commit": restored_commit, "document": self.read_document(relative_path)}

    def delete_document(self, relative_path: str, author: str) -> None:
        relative_path = validate_relative_path(relative_path)
        suffix = Path(relative_path).suffix.lower()
        if suffix not in {".md", ".json"}:
            raise ValueError("document path must end in .md or .json")
        if Path(relative_path).name in RESERVED_DOCUMENTS:
            raise ValueError(f"{Path(relative_path).name} is reserved by OKF")
        path = self.repository / relative_path
        if not path.is_file():
            raise FileNotFoundError(relative_path)
        path.unlink()
        self.git.commit([relative_path], f"Delete {relative_path}", author)

    def move_document(self, relative_path: str, target_folder: str, author: str) -> dict[str, Any]:
        relative_path = validate_relative_path(relative_path)
        suffix = Path(relative_path).suffix.lower()
        if suffix not in {".md", ".json"}:
            raise ValueError("document path must end in .md or .json")
        if Path(relative_path).name in RESERVED_DOCUMENTS:
            raise ValueError(f"{Path(relative_path).name} is reserved by OKF")
        clean_folder = validate_relative_path(target_folder) if target_folder else ""
        source = self.repository / relative_path
        if not source.is_file():
            raise FileNotFoundError(relative_path)
        destination_folder = self.repository / clean_folder if clean_folder else self.repository
        if not destination_folder.is_dir():
            raise FileNotFoundError(clean_folder)
        destination_relative = (Path(clean_folder) / source.name).as_posix() if clean_folder else source.name
        destination = self.repository / destination_relative
        if destination == source:
            return self.read_document(relative_path)
        if destination.exists():
            raise FileExistsError(destination_relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.rename(destination)
        self.git.commit([relative_path, destination_relative], f"Move {relative_path} to {destination_relative}", author)
        return self.read_document(destination_relative)

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

    def delete_folder(self, relative_path: str, author: str) -> None:
        clean = validate_relative_path(relative_path)
        if not clean:
            raise ValueError("root folder cannot be deleted")
        documents = [document for document in self.list_documents() if document["folder"] == clean or document["folder"].startswith(f"{clean}/")]
        if documents:
            raise ValueError("folder contains documents")
        folder = self.repository / clean
        schema_path = folder / SCHEMA_FILE
        if not folder.exists():
            raise FileNotFoundError(clean)
        removed_paths: list[str] = []
        if schema_path.exists():
            schema_path.unlink()
            removed_paths.append(f"{clean}/{SCHEMA_FILE}")
        try:
            folder.rmdir()
        except OSError as exc:
            raise ValueError("folder is not empty") from exc
        if not removed_paths:
            self.git.commit([clean], f"Delete folder {clean}", author)
        else:
            self.git.commit(removed_paths, f"Delete folder {clean}", author)

    def move_folder(self, relative_path: str, target_parent: str, author: str) -> dict[str, str]:
        clean = validate_relative_path(relative_path)
        if not clean:
            raise ValueError("root folder cannot be moved")
        parent = validate_relative_path(target_parent) if target_parent else ""
        if parent == clean:
            raise ValueError("folder cannot be moved into itself")
        if parent.startswith(f"{clean}/"):
            raise ValueError("folder cannot be moved into one of its descendants")
        source = self.repository / clean
        if not source.is_dir():
            raise FileNotFoundError(clean)
        destination_relative = (Path(parent) / source.name).as_posix() if parent else source.name
        destination = self.repository / destination_relative
        if destination == source:
            return {"path": clean}
        if destination.exists():
            raise FileExistsError(destination_relative)
        if parent and not (self.repository / parent).is_dir():
            raise FileNotFoundError(parent)
        old_paths = [path.relative_to(self.repository).as_posix() for path in source.rglob("*") if path.is_file()]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        new_paths = [f"{destination_relative}/{Path(path).relative_to(clean).as_posix()}" for path in old_paths]
        self.git.commit([*old_paths, *new_paths], f"Move folder {clean} to {destination_relative}", author)
        return {"path": destination_relative}

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
        return {"path": clean, "schema": schema, "inherited_schema": self._merged_schema(clean, include_current=False), "effective_schema": self._merged_schema(clean)}

    def save_schema(self, folder: str, schema: dict[str, Any], author: str) -> dict[str, Any]:
        clean = validate_relative_path(folder) if folder else ""
        if not isinstance(schema, dict):
            raise ValueError("schema must be a mapping")
        governance_errors = self._governance_errors(self._merged_schema(clean, include_current=False) | schema)
        if governance_errors:
            raise ValueError("; ".join(governance_errors))
        path = self.repository / clean / SCHEMA_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(schema, sort_keys=False), encoding="utf-8")
        relative = path.relative_to(self.repository).as_posix()
        self.git.commit([relative], f"Update schema for {clean or 'root'}", author)
        return self.read_schema(clean)

    def _merged_schema(self, folder: str, include_current: bool = True) -> dict[str, Any]:
        folders = [""]
        current = Path()
        for part in Path(folder).parts:
            current /= part
            folders.append(current.as_posix())
        if not include_current:
            folders = folders[:-1]
        merged: dict[str, Any] = {}
        for candidate in folders:
            path = self.repository / candidate / SCHEMA_FILE
            if path.exists():
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                if not isinstance(data, dict):
                    raise ValueError(f"{path.relative_to(self.repository)} must contain a YAML mapping")
                merged = merge_metadata(merged, data)
        return merged

    def _governance_errors(self, metadata: dict[str, Any]) -> list[str]:
        validation = validate_governance(metadata)
        errors = list(validation.errors)
        scope_id = metadata.get("scope_id")
        if scope_id and scope_id not in {scope["id"] for scope in self.list_scopes()}:
            errors.append(f"scope_id: unknown scope {scope_id}")
        return errors

    def validation_report(self) -> dict[str, Any]:
        documents = self.list_documents()
        invalid = [document for document in documents if not document["validation"]["valid"]]
        return {"valid": not invalid, "total": len(documents), "invalid": len(invalid), "documents": invalid}

    def list_scopes(self) -> list[dict[str, Any]]:
        path = self.repository / SCOPES_FILE
        signature = path.stat().st_mtime_ns if path.exists() else None
        if self._scopes_cache and self._scopes_cache[0] == signature:
            return [dict(item) for item in self._scopes_cache[1]]
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {} if path.exists() else {}
        nodes = [ScopeNode.model_validate(item) for item in data.get("scopes", [])]
        scopes = [node.model_dump() for node in nodes]
        self._scopes_cache = (signature, scopes)
        return [dict(item) for item in scopes]

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
        self._scopes_cache = (path.stat().st_mtime_ns, [dict(item) for item in scopes])
