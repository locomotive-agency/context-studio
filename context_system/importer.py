from __future__ import annotations

import base64
import binascii
import json
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from .cms import ContentStore
from .config import Config, get_config
from .okf import RESERVED_DOCUMENTS, SCHEMA_FILE, load_effective_schema, merge_metadata, parse_document, validate_frontmatter, validate_governance

IMPORTABLE_RESERVED = {SCHEMA_FILE, "_scopes.yaml", "index.md", "log.md"}


class OKFImporter:
    def __init__(self, config: Config | None = None):
        self.config = config or get_config()

    def scan(self, source_folder: str | Path) -> dict[str, Any]:
        source = Path(source_folder)
        blockers: list[dict[str, str]] = []
        warnings: list[dict[str, str]] = []
        files: list[dict[str, str]] = []
        if not source.is_dir():
            return {"source_folder": str(source), "files": [], "blockers": [{"path": "", "message": "source folder not found"}], "warnings": []}
        seen: set[str] = set()
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            if ".git" in path.parts:
                continue
            relative = path.relative_to(source).as_posix()
            try:
                PurePosixPath(relative)
                if ".." in PurePosixPath(relative).parts:
                    raise ValueError("path must stay within import folder")
            except ValueError as exc:
                blockers.append({"path": relative, "message": str(exc)})
                continue
            if relative in seen:
                blockers.append({"path": relative, "message": "duplicate path in import"})
                continue
            seen.add(relative)
            name = path.name
            suffix = path.suffix.lower()
            if name in IMPORTABLE_RESERVED:
                self._validate_reserved(path, source, relative, blockers)
                files.append({"path": relative, "kind": name})
                continue
            if suffix == ".md":
                self._validate_markdown(path, source, relative, blockers)
                files.append({"path": relative, "kind": "markdown"})
                continue
            if suffix == ".json":
                self._validate_json(path, relative, blockers)
                files.append({"path": relative, "kind": "json"})
                continue
            warnings.append({"path": relative, "message": "file type skipped"})
        return {"source_folder": str(source), "files": files, "blockers": blockers, "warnings": warnings}

    def scan_uploaded(self, folder_name: str, uploaded_files: list[dict[str, Any]]) -> dict[str, Any]:
        with tempfile.TemporaryDirectory(prefix="okf-import-") as temporary:
            self._write_uploaded_files(Path(temporary), uploaded_files)
            plan = self.scan(temporary)
        plan["source_folder"] = folder_name.strip() or "uploaded-folder"
        return plan

    def apply_uploaded(self, folder_name: str, uploaded_files: list[dict[str, Any]], author: str) -> dict[str, Any]:
        display_name = folder_name.strip() or "uploaded-folder"
        with tempfile.TemporaryDirectory(prefix="okf-import-") as temporary:
            source = Path(temporary)
            self._write_uploaded_files(source, uploaded_files)
            import_plan = self.scan(source)
            blockers = import_plan.get("blockers", [])
            if blockers:
                raise ValueError("import plan has blockers")
            imported = []
            for item in sorted(import_plan.get("files", []), key=lambda row: row["path"]):
                relative = item["path"]
                source_path = source / relative
                target_path = self.config.context_repo / relative
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source_path, target_path)
                imported.append(relative)
        commit = ContentStore(self.config.context_repo).git.commit(imported, f"Import OKF folder {display_name}", author)
        return {"imported_files": imported, "commit": commit}

    def apply(self, import_plan: dict[str, Any], author: str) -> dict[str, Any]:
        blockers = import_plan.get("blockers", [])
        if blockers:
            raise ValueError("import plan has blockers")
        source = Path(import_plan["source_folder"])
        if not source.is_dir():
            raise ValueError("source folder not found")
        imported = []
        for item in sorted(import_plan.get("files", []), key=lambda row: row["path"]):
            relative = item["path"]
            source_path = source / relative
            target_path = self.config.context_repo / relative
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)
            imported.append(relative)
        commit = ContentStore(self.config.context_repo).git.commit(imported, f"Import OKF folder {source.name}", author)
        return {"imported_files": imported, "commit": commit}

    def _write_uploaded_files(self, destination: Path, uploaded_files: list[dict[str, Any]]) -> None:
        if not uploaded_files:
            raise ValueError("files are required")
        for uploaded in uploaded_files:
            relative = self._uploaded_relative_path(uploaded.get("path", ""))
            content = self._uploaded_content(uploaded, relative)
            if content is None:
                raise ValueError(f"content is required for {relative}")
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)

    @staticmethod
    def _uploaded_content(uploaded: dict[str, Any], relative: str) -> bytes | None:
        encoded = uploaded.get("content_base64")
        if encoded is not None:
            if not isinstance(encoded, str):
                raise ValueError(f"content_base64 must be a string for {relative}")
            try:
                return base64.b64decode(encoded)
            except (binascii.Error, ValueError) as exc:
                raise ValueError(f"content_base64 must be valid base64 for {relative}") from exc
        content = uploaded.get("content")
        if content is None:
            return None
        return str(content).encode("utf-8")

    @staticmethod
    def _uploaded_relative_path(value: str) -> str:
        raw_path = str(value).replace("\\", "/").strip()
        path = PurePosixPath(raw_path)
        first_part = path.parts[0] if path.parts else ""
        if (
            not raw_path
            or path.is_absolute()
            or ":" in first_part
            or ".." in path.parts
            or ".git" in path.parts
        ):
            raise ValueError("uploaded paths must be relative and stay within the selected folder")
        return path.as_posix()

    def _validate_reserved(self, path: Path, source: Path, relative: str, blockers: list[dict[str, str]]) -> None:
        if path.name in {SCHEMA_FILE, "_scopes.yaml"}:
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError as exc:
                blockers.append({"path": relative, "message": f"invalid YAML: {exc}"})
                return
            if not isinstance(data, dict):
                blockers.append({"path": relative, "message": "YAML file must contain a mapping"})

    def _validate_markdown(self, path: Path, source: Path, relative: str, blockers: list[dict[str, str]]) -> None:
        if path.name in RESERVED_DOCUMENTS:
            return
        try:
            parsed = parse_document(path.read_text(encoding="utf-8"))
            effective = merge_metadata(load_effective_schema(source, relative), parsed.frontmatter)
            frontmatter_validation = validate_frontmatter(effective)
            governance_validation = validate_governance(effective)
        except ValueError as exc:
            blockers.append({"path": relative, "message": str(exc)})
            return
        for error in frontmatter_validation.errors + governance_validation.errors:
            blockers.append({"path": relative, "message": error})

    @staticmethod
    def _validate_json(path: Path, relative: str, blockers: list[dict[str, str]]) -> None:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            blockers.append({"path": relative, "message": f"invalid JSON: {exc.msg} at line {exc.lineno}"})
