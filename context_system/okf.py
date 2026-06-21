from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

from .models import GovernanceMetadata

SCHEMA_FILE = "_schema.yaml"
RESERVED_DOCUMENTS = {"index.md", "log.md"}
SUPPORTING_SOURCE_KEYS = ("collections", "web", "mcp")


class OKFFrontmatter(BaseModel):
    type: str = Field(min_length=1)
    title: str | None = None
    description: str | None = None
    resource: str | None = None
    tags: list[str] = Field(default_factory=list)
    timestamp: str | None = None

    model_config = {"extra": "allow"}

    @field_validator("type")
    @classmethod
    def type_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("type must not be blank")
        return value.strip()


class DocumentValidation(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)


class ParsedDocument(BaseModel):
    frontmatter: dict[str, Any]
    body: str


def parse_document(text: str) -> ParsedDocument:
    if not text.startswith("---\n"):
        raise ValueError("document must start with YAML frontmatter delimited by ---")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("document frontmatter is missing its closing --- delimiter")
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return ParsedDocument(frontmatter=frontmatter, body=parts[2].lstrip("\n"))


def render_document(frontmatter: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False).strip()
    return f"---\n{yaml_text}\n---\n\n{body.rstrip()}\n"


def normalize_supporting_sources(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    normalized: dict[str, list[str]] = {}
    for key in SUPPORTING_SOURCE_KEYS:
        items = value.get(key, [])
        if isinstance(items, str):
            items = [items]
        if not isinstance(items, list):
            continue
        cleaned = []
        for item in items:
            if isinstance(item, str) and item.strip():
                cleaned.append(item.strip())
        if cleaned:
            normalized[key] = cleaned
    return normalized


def merge_supporting_sources(left: Any, right: Any) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for source in (normalize_supporting_sources(left), normalize_supporting_sources(right)):
        for key, values in source.items():
            bucket = merged.setdefault(key, [])
            for value in values:
                if value not in bucket:
                    bucket.append(value)
    return merged


def merge_metadata(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    base_sources = base.get("supporting_sources")
    override_sources = override.get("supporting_sources")
    merged.update(override)
    sources = merge_supporting_sources(base_sources, override_sources)
    if sources:
        merged["supporting_sources"] = sources
    return merged


def validate_frontmatter(frontmatter: dict[str, Any]) -> DocumentValidation:
    try:
        OKFFrontmatter.model_validate(frontmatter)
    except ValidationError as exc:
        errors = [f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}" for error in exc.errors()]
        return DocumentValidation(valid=False, errors=errors)
    return DocumentValidation(valid=True)


def validate_governance(metadata: dict[str, Any]) -> DocumentValidation:
    try:
        GovernanceMetadata.model_validate(metadata)
    except ValidationError as exc:
        errors = [f"{'.'.join(str(part) for part in error['loc']) or 'governance'}: {error['msg']}" for error in exc.errors()]
        return DocumentValidation(valid=False, errors=errors)
    return DocumentValidation(valid=True)


def validate_relative_path(value: str, *, suffix: str | None = None) -> str:
    path = PurePosixPath(value.strip("/"))
    if not value or path.is_absolute() or ".." in path.parts:
        raise ValueError("path must stay within the context repository")
    if suffix and path.suffix.lower() != suffix:
        raise ValueError(f"path must end in {suffix}")
    return path.as_posix()


def schema_paths(repository: Path, document_path: str) -> list[Path]:
    relative = PurePosixPath(document_path)
    directories = [PurePosixPath()]
    current = PurePosixPath()
    for part in relative.parent.parts:
        current /= part
        directories.append(current)
    return [repository / directory / SCHEMA_FILE for directory in directories]


def load_effective_schema(repository: Path, document_path: str) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for path in schema_paths(repository, document_path):
        if not path.exists():
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            raise ValueError(f"{path.relative_to(repository)} must contain a YAML mapping")
        merged = merge_metadata(merged, data)
    return merged
