from __future__ import annotations

from datetime import date
from pathlib import Path

from .audit import AuditLog
from .config import Config, get_config
from .models import ContextPackage, MissingContextBlock, StalenessFlag
from .repository import ContextRepository


class ContextService:
    def __init__(self, config: Config | None = None):
        self.config = config or get_config()
        self.repository = ContextRepository(self.config)
        self.audit = AuditLog(self.config.audit_db)

    def get_construct(self, construct: str, scope_id: str | None = None) -> list[dict]:
        return [record.model_dump() for record in self.repository.get_construct(construct, scope_id=scope_id)]

    def search(self, query: str, constructs: list[str] | None = None, top_k: int = 5) -> list[dict]:
        return [pointer.model_dump() for pointer in self.repository.search(query, constructs, top_k)]

    def assemble_context_package(
        self,
        task: str,
        constructs: list[str],
        scope: dict | None = None,
        icp: str | None = None,
        run_id: str | None = None,
        query: str | None = None,
    ) -> ContextPackage:
        pkg = ContextPackage(task=task)
        pkg.kb_git_sha = self.repository.content.git.head()
        scope_id = (scope or {}).get("id") or (scope or {}).get("scope_id")
        controlled_used: list[dict] = []
        for construct in constructs:
            records = self.repository.get_construct(construct, scope_id=scope_id)
            if not records:
                pkg.missing_blocks.append(
                    MissingContextBlock(
                        construct=construct,
                        reason="no approved records",
                        blocks_workflow=False,
                    )
                )
                continue
            for record in records:
                data = record.model_dump()
                if record.criticality == "controlled":
                    if not (self.config.context_repo / record.kb_path).exists() or not record.body.strip():
                        pkg.missing_blocks.append(
                            MissingContextBlock(
                                construct=construct,
                                reason=f"controlled record {record.id} has no body",
                            )
                        )
                        continue
                    if record.exact_language:
                        pkg.exact_language_map[record.id] = record.body
                    controlled_used.append(data)
                pkg.records.append(data)
            pkg.staleness_flags.extend(self._staleness([record.model_dump() for record in records]))

        if query:
            pkg.search_pointers = self.repository.search(query, constructs)
        if controlled_used and run_id:
            self.audit.write(
                run_id=run_id,
                task=task,
                record_ids=[record["id"] for record in controlled_used],
                hashes=[record["content_hash"] for record in controlled_used],
            )
        return pkg

    def stats(self) -> dict:
        stats = self.repository.stats()
        stats["recent_controlled_uses"] = self.audit.recent(limit=5)
        return stats

    def _staleness(self, records: list[dict]) -> list[StalenessFlag]:
        flags: list[StalenessFlag] = []
        today = date.today()
        for record in records:
            verified = record.get("date_verified")
            if not verified:
                continue
            overdue = (today - date.fromisoformat(verified)).days - record["staleness_threshold_days"]
            if overdue > 0:
                flags.append(
                    StalenessFlag(
                        record_id=record["id"],
                        days_overdue=overdue,
                        message=f"{record['id']} is {overdue} days past its freshness window",
                    )
                )
        return flags
