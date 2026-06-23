from __future__ import annotations

from datetime import date

from .cms import ContentStore
from .config import Config, get_config
from .models import ContextRecord, RuntimeRecord
from .okf import parse_document, parse_markdown_metadata


class ContextRepository:
    def __init__(self, config: Config | None = None):
        self.config = config or get_config()
        self.content = ContentStore(self.config.context_repo)
        self._runtime_cache: dict[bool, tuple[tuple[tuple[str, int, int], ...], list[RuntimeRecord]]] = {}

    def runtime_records(self, include_body: bool = True) -> list[RuntimeRecord]:
        signature = self._content_signature()
        cached = self._runtime_cache.get(include_body)
        if cached and cached[0] == signature:
            return list(cached[1])
        records = []
        for document in self.content.list_documents():
            if document.get("format") != "markdown" or not document["validation"]["valid"]:
                continue
            full_document = self.content.read_document(document["path"], include_body=include_body)
            definition = self._definition(full_document)
            records.append(self._runtime_record(definition, full_document))
        self._runtime_cache[include_body] = (signature, records)
        return records

    def stats(self) -> dict:
        records = self.runtime_records(include_body=False)
        report = self.content.validation_report()
        return {
            "total_records": report["total"],
            "valid_records": report["total"] - report["invalid"],
            "invalid_records": report["invalid"],
            "controlled_records": sum(record.criticality == "controlled" for record in records),
            "hybrid_records": sum(record.criticality == "hybrid" for record in records),
            "flexible_records": sum(record.criticality == "flexible" for record in records),
            "git_sha": self.content.git.head(),
        }

    def _definition(self, document: dict) -> ContextRecord:
        metadata = document["effective_frontmatter"] | {"kb_glob": document["path"]}
        metadata.setdefault("id", document["path"].removesuffix(".md").replace("/", "."))
        metadata.setdefault("title", document["name"].replace("-", " ").title())
        return ContextRecord.model_validate(metadata)

    def _content_signature(self) -> tuple[tuple[str, int, int], ...]:
        items = []
        for path in sorted([*self.config.context_repo.rglob("*.md"), *self.config.context_repo.rglob("*.json")]):
            if ".git" in path.parts:
                continue
            stat = path.stat()
            items.append((path.relative_to(self.config.context_repo).as_posix(), stat.st_mtime_ns, stat.st_size))
        return tuple(items)

    def _runtime_record(self, definition: ContextRecord, document: dict) -> RuntimeRecord:
        path = self.config.context_repo / document["path"]
        body = document["body"]
        if not body and path.suffix.lower() == ".md":
            try:
                body = parse_document(path.read_text(encoding="utf-8")).body
            except ValueError:
                body = ""
        markdown = parse_markdown_metadata(body, document["path"])
        return RuntimeRecord(
            id=definition.id,
            title=definition.title,
            type=definition.type,
            durability=definition.durability,
            provenance=definition.provenance,
            criticality=definition.criticality,
            status=definition.status,
            kb_path=document["path"],
            content_hash=__import__("hashlib").sha256(path.read_bytes()).hexdigest()[:16],
            valid_until=definition.valid_until.isoformat() if definition.valid_until else None,
            scope=definition.scope.model_dump(exclude_none=True),
            scope_id=definition.scope_id,
            checks=definition.checks,
            okf={"type": definition.type, "title": definition.title, "description": definition.description, "resource": definition.resource, "tags": definition.tags},
            supporting_sources=definition.supporting_sources,
            links=markdown.internal_links,
            external_links=markdown.external_links,
            citations=markdown.citations,
            headings=markdown.headings,
            body=document["body"],
        )

    @staticmethod
    def _is_current(record: RuntimeRecord) -> bool:
        today = date.today()
        if record.valid_until and date.fromisoformat(record.valid_until) < today:
            return False
        return True

    def _scope_matches(self, record_scope_id: str | None, requested_scope_id: str | None) -> bool:
        if not record_scope_id:
            return True
        if not requested_scope_id:
            return True
        try:
            return record_scope_id in self.content.scope_ancestors(requested_scope_id)
        except ValueError:
            return False

    @staticmethod
    def _extend_sources(target: dict[str, list[str]], sources: dict) -> None:
        if not isinstance(sources, dict):
            return
        for key in ("collections", "web", "mcp"):
            values = sources.get(key, [])
            if isinstance(values, str):
                values = [values]
            if not isinstance(values, list):
                continue
            bucket = target.setdefault(key, [])
            for value in values:
                if isinstance(value, str) and value and value not in bucket:
                    bucket.append(value)
