from __future__ import annotations

from datetime import date

from .cms import ContentStore
from .config import Config, get_config
from .models import ContextRecord, Criticality, RuntimeRecord, SearchPointer
from .okf import parse_markdown_metadata


class ContextRepository:
    def __init__(self, config: Config | None = None):
        self.config = config or get_config()
        self.content = ContentStore(self.config.context_repo)

    def runtime_records(self, include_body: bool = True) -> list[RuntimeRecord]:
        records = []
        for document in self.content.list_documents():
            if document.get("format") != "markdown" or not document["validation"]["valid"]:
                continue
            full_document = self.content.read_document(document["path"], include_body=include_body)
            definition = self._definition(full_document)
            records.append(self._runtime_record(definition, full_document))
        return records

    def get_construct(self, construct: str, include_body: bool = True, scope_id: str | None = None) -> list[RuntimeRecord]:
        records = [record for record in self.runtime_records(include_body) if record.type == construct and record.status == "approved" and self._is_current(record)]
        if not scope_id:
            return records
        ancestors = self.content.scope_ancestors(scope_id)
        eligible = [record for record in records if not record.scope_id or record.scope_id in ancestors]
        if not eligible:
            return []
        rank = {scope: index + 1 for index, scope in enumerate(ancestors)}
        highest = max(rank.get(record.scope_id, 0) for record in eligible)
        return [record for record in eligible if rank.get(record.scope_id, 0) == highest]

    def search(self, query: str, constructs: list[str] | None = None, top_k: int = 5) -> list[SearchPointer]:
        return []

    def resolve_criticality(self, construct: str, scope_id: str | None = None) -> Criticality:
        candidates: list[Criticality] = [record.criticality for record in self.get_construct(construct, include_body=False, scope_id=scope_id)]
        for folder in self.content.list_folders():
            schema = folder["effective_schema"]
            if schema.get("type") != construct:
                continue
            if not self._scope_matches(schema.get("scope_id"), scope_id):
                continue
            criticality = schema.get("criticality")
            if criticality in {"controlled", "hybrid", "flexible"}:
                candidates.append(criticality)
        if not candidates:
            return "flexible"
        rank = {"flexible": 0, "hybrid": 1, "controlled": 2}
        return max(candidates, key=lambda value: rank[value])

    def supporting_sources_for(self, construct: str, scope_id: str | None = None) -> dict[str, list[str]]:
        merged: dict[str, list[str]] = {}
        for folder in self.content.list_folders():
            schema = folder["effective_schema"]
            if schema.get("type") != construct or not self._scope_matches(schema.get("scope_id"), scope_id):
                continue
            self._extend_sources(merged, schema.get("supporting_sources", {}))
        for record in self.get_construct(construct, include_body=False, scope_id=scope_id):
            self._extend_sources(merged, record.supporting_sources)
        return merged

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

    def _runtime_record(self, definition: ContextRecord, document: dict) -> RuntimeRecord:
        path = self.config.context_repo / document["path"]
        markdown = parse_markdown_metadata(document["body"], document["path"])
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
