from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from .git_store import GitStore
from .okf import SCHEMA_FILE, merge_metadata, validate_governance, validate_relative_path


class SchemaStore:
    def __init__(self, repository: Path, git: GitStore, scope_ids: Callable[[], set[str]]):
        self.repository = repository
        self.git = git
        self.scope_ids = scope_ids

    def read_schema(self, folder: str) -> dict[str, Any]:
        clean = validate_relative_path(folder) if folder else ""
        path = self.repository / clean / SCHEMA_FILE
        schema = yaml.safe_load(path.read_text(encoding="utf-8")) or {} if path.exists() else {}
        return {
            "path": clean,
            "schema": schema,
            "inherited_schema": self.merged_schema(clean, include_current=False),
            "effective_schema": self.merged_schema(clean),
        }

    def save_schema(self, folder: str, schema: dict[str, Any], author: str) -> dict[str, Any]:
        clean = validate_relative_path(folder) if folder else ""
        if not isinstance(schema, dict):
            raise ValueError("schema must be a mapping")
        governance_errors = self._governance_errors(self.merged_schema(clean, include_current=False) | schema)
        if governance_errors:
            raise ValueError("; ".join(governance_errors))
        path = self.repository / clean / SCHEMA_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(schema, sort_keys=False), encoding="utf-8")
        relative = path.relative_to(self.repository).as_posix()
        self.git.commit([relative], f"Update schema for {clean or 'root'}", author)
        return self.read_schema(clean)

    def merged_schema(self, folder: str, include_current: bool = True) -> dict[str, Any]:
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
        if scope_id and scope_id not in self.scope_ids():
            errors.append(f"scope_id: unknown scope {scope_id}")
        return errors
