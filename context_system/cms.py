from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

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
from .schema_store import SchemaStore
from .scope_store import ScopeStore


class ContentStore:
    def __init__(self, repository: Path):
        self.repository = repository
        self.git = GitStore(repository)
        self.scopes = ScopeStore(repository, self.git)
        self.schemas = SchemaStore(repository, self.git, lambda: {scope["id"] for scope in self.list_scopes()})

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
        return self.schemas.read_schema(folder)

    def save_schema(self, folder: str, schema: dict[str, Any], author: str) -> dict[str, Any]:
        return self.schemas.save_schema(folder, schema, author)

    def _merged_schema(self, folder: str, include_current: bool = True) -> dict[str, Any]:
        return self.schemas.merged_schema(folder, include_current)

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
        return self.scopes.list_scopes()

    def save_scope(self, data: dict[str, Any], author: str, existing_id: str | None = None) -> dict[str, Any]:
        return self.scopes.save_scope(data, author, existing_id)

    def reorder_scopes(self, parent_id: str | None, ordered_ids: list[str], author: str) -> list[dict[str, Any]]:
        return self.scopes.reorder_scopes(parent_id, ordered_ids, author)

    def move_scope(self, scope_id: str, parent_id: str | None, index: int, author: str) -> list[dict[str, Any]]:
        return self.scopes.move_scope(scope_id, parent_id, index, author)

    def delete_scope(self, scope_id: str, author: str) -> None:
        assigned = {document["effective_frontmatter"].get("scope_id") for document in self.list_documents()}
        self.scopes.delete_scope(scope_id, author, {scope_id for scope_id in assigned if scope_id})

    def scope_ancestors(self, scope_id: str) -> list[str]:
        return self.scopes.scope_ancestors(scope_id)
