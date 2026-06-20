from __future__ import annotations

import math
import re
from collections import Counter
from datetime import date

from .cms import ContentStore
from .config import Config, get_config
from .models import ContextRecord, RuntimeRecord, SearchPointer

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


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
        if not query.strip() or top_k <= 0:
            return []
        allowed = set(constructs or [])
        records = [record for record in self.runtime_records() if record.criticality != "controlled" and self._is_current(record) and (not allowed or record.type in allowed)]
        if not records:
            return []
        doc_tokens = [tokenize(record.body) for record in records]
        frequencies: Counter[str] = Counter()
        for tokens in doc_tokens:
            frequencies.update(set(tokens))
        idf = {term: math.log((1 + len(records)) / (1 + count)) + 1 for term, count in frequencies.items()}
        query_vector = self._tfidf(Counter(tokenize(query)), idf)
        scored = []
        for record, tokens in zip(records, doc_tokens):
            score = self._cosine(query_vector, self._tfidf(Counter(tokens), idf))
            if score > 0:
                scored.append(SearchPointer(record_id=record.id, kb_path=record.kb_path, score=round(score, 6), type=record.type))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]

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
            edit_roles=definition.edit_roles,
            scope=definition.scope.model_dump(exclude_none=True),
            scope_id=definition.scope_id,
            checks=definition.checks,
            okf={"type": definition.type, "title": definition.title, "description": definition.description, "resource": definition.resource, "tags": definition.tags},
            body=document["body"],
        )

    @staticmethod
    def _is_current(record: RuntimeRecord) -> bool:
        today = date.today()
        if record.valid_until and date.fromisoformat(record.valid_until) < today:
            return False
        return True

    def _tfidf(self, counts: Counter[str], idf: dict[str, float]) -> dict[str, float]:
        total = sum(counts.values()) or 1
        return {term: count / total * idf.get(term, 0) for term, count in counts.items()}

    def _cosine(self, left: dict[str, float], right: dict[str, float]) -> float:
        dot = sum(weight * right.get(term, 0) for term, weight in left.items())
        if not dot:
            return 0
        return dot / (math.sqrt(sum(value * value for value in left.values())) * math.sqrt(sum(value * value for value in right.values())))
