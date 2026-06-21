from __future__ import annotations

import json
import shutil
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
