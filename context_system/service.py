from __future__ import annotations

from pathlib import Path

from .audit import AuditLog
from .collections import CollectionManager
from .config import Config, get_config
from .models import ContextPackage, ContextPackageResponse, MissingContextBlock
from .importer import OKFImporter
from .repository import ContextRepository


class ContextService:
    def __init__(self, config: Config | None = None):
        self.config = config or get_config()
        self.repository = ContextRepository(self.config)
        self.collections = CollectionManager(self.config)
        self.importer = OKFImporter(self.config)
        self.audit = AuditLog(self.config.audit_db)

    def get_construct(self, construct: str, scope_id: str | None = None) -> list[dict]:
        return [record.model_dump() for record in self.repository.get_construct(construct, scope_id=scope_id)]

    def search(self, query: str, constructs: list[str] | None = None, top_k: int = 5) -> list[dict]:
        return [pointer.model_dump() for pointer in self.repository.search(query, constructs, top_k)]

    def assemble_context_package(
        self,
        task: str,
        scope_id: str | None,
        requests: list[dict],
        run_id: str | None = None,
        user: dict | None = None,
    ) -> dict:
        package = {
            "task": task,
            "scope_id": scope_id,
            "results": [],
            "blocked": False,
            "kb_git_sha": self.repository.content.git.head(),
        }
        if run_id:
            package["run_id"] = run_id
        controlled_used: list[dict] = []
        for item in requests:
            construct = str(item.get("type", "")).strip()
            query = item.get("query")
            if not construct:
                continue
            resolved = self.repository.resolve_criticality(construct, scope_id=scope_id)
            records = self.repository.get_construct(construct, scope_id=scope_id)
            okf_records = [record.model_dump() for record in records]
            missing = []
            collection_results: list[dict] = []
            suggested_sources: list[dict] = []
            access_issues: list[dict] = []
            if resolved == "controlled":
                if not records:
                    missing.append(
                        MissingContextBlock(
                            type=construct,
                            reason="missing approved controlled context",
                            blocks_workflow=True,
                        ).model_dump()
                    )
                for record in records:
                    if not record.body.strip():
                        missing.append(
                            MissingContextBlock(
                                type=construct,
                                reason=f"controlled record {record.id} has no body",
                                blocks_workflow=True,
                            ).model_dump()
                        )
                    else:
                        controlled_used.append(record.model_dump())
            else:
                sources = self.repository.supporting_sources_for(construct, scope_id=scope_id)
                if query and sources.get("collections"):
                    collection_results = self.collections.search(sources["collections"], str(query), top_k=5)
                suggested_sources.extend({"kind": "web", "value": url} for url in sources.get("web", []))
                allowed_mcp, denied_mcp = self._rbac_mcp_sources(sources.get("mcp", []), user)
                suggested_sources.extend({"kind": "mcp", "value": value} for value in allowed_mcp)
                access_issues.extend(denied_mcp)
            package["results"].append(
                {
                    "type": construct,
                    "resolved_criticality": resolved,
                    "okf_records": okf_records,
                    "collection_results": collection_results,
                    "suggested_sources": suggested_sources,
                    "missing": missing,
                    "access_issues": access_issues,
                }
            )
            if any(block["blocks_workflow"] for block in missing):
                package["blocked"] = True
        if controlled_used and run_id:
            self.audit.write(
                run_id=run_id,
                task=task,
                record_ids=[record["id"] for record in controlled_used],
                hashes=[record["content_hash"] for record in controlled_used],
            )
        return ContextPackageResponse.model_validate(package).model_dump(exclude_none=True)

    def assemble_construct_context_package(
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
                        type=construct,
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
                                type=construct,
                                reason=f"controlled record {record.id} has no body",
                            )
                        )
                        continue
                    controlled_used.append(data)
                pkg.records.append(data)
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

    def scan_okf_folder(self, source_folder: str | Path) -> dict:
        return self.importer.scan(source_folder)

    def import_okf_folder(self, source_folder: str | Path, author: str) -> dict:
        plan = self.importer.scan(source_folder)
        return self.importer.apply(plan, author)

    def stats(self) -> dict:
        stats = self.repository.stats()
        stats["recent_controlled_uses"] = self.audit.recent(limit=5)
        return stats

    def _rbac_mcp_sources(self, sources: list[str], user: dict | None) -> tuple[list[str], list[dict]]:
        allowed: list[str] = []
        denied: list[dict] = []
        if user is None and not self.config.mcp_service_account_role:
            return [], [{"kind": "mcp", "value": source, "reason": "missing authenticated user"} for source in sources]
        role = (user or {"role": self.config.mcp_service_account_role}).get("role")
        configured = self.config.mcp_servers
        for source in sources:
            policy = self._mcp_policy(source, configured)
            if policy is None:
                if configured:
                    denied.append({"kind": "mcp", "value": source, "reason": "not configured"})
                else:
                    allowed.append(source)
                continue
            roles = policy.get("roles") or ["viewer", "editor", "admin"]
            if role in roles:
                allowed.append(source)
            else:
                denied.append({"kind": "mcp", "value": source, "reason": "insufficient role"})
        return allowed, denied

    @staticmethod
    def _mcp_policy(source: str, configured: list[str | dict]) -> dict | None:
        for item in configured:
            if isinstance(item, str) and item == source:
                return {"id": item, "roles": ["viewer", "editor", "admin"]}
            if isinstance(item, dict) and source in {item.get("id"), item.get("url")}:
                return item
        return None
