from __future__ import annotations

from pathlib import Path

from .audit import AuditLog
from .collections import CollectionManager
from .config import Config, get_config
from .importer import OKFImporter
from .repository import ContextRepository


class ContextService:
    def __init__(self, config: Config | None = None):
        self.config = config or get_config()
        self.repository = ContextRepository(self.config)
        self.collections = CollectionManager(self.config)
        self.importer = OKFImporter(self.config)
        self.audit = AuditLog(self.config.audit_db)

    def list_context_scopes(self) -> list[dict]:
        return self.repository.content.list_scopes()

    def list_context_types(self, scope_id: str | None = None) -> list[str]:
        types = {
            record.type
            for record in self.repository.runtime_records(include_body=False)
            if record.status == "approved" and self.repository._is_current(record) and self._record_visible_for_scope(record, scope_id)
        }
        for folder in self.repository.content.list_folders():
            schema = folder["effective_schema"]
            type_name = schema.get("type")
            if isinstance(type_name, str) and type_name and self.repository._scope_matches(schema.get("scope_id"), scope_id):
                types.add(type_name)
        return sorted(types)

    def list_context_folders(self, type: str | None = None, scope_id: str | None = None) -> list[dict]:
        records = [
            record
            for record in self.repository.runtime_records(include_body=False)
            if record.status == "approved"
            and self.repository._is_current(record)
            and (not type or record.type == type)
            and self._record_visible_for_scope(record, scope_id)
        ]
        folder_paths: set[str] = set()
        for record in records:
            parent = Path(record.kb_path).parent
            while str(parent) != ".":
                folder_paths.add(parent.as_posix())
                parent = parent.parent
        folders = []
        for path in sorted(folder_paths):
            schema = self.repository.content.read_schema(path)
            direct_records = [record for record in records if Path(record.kb_path).parent.as_posix() == path]
            nested_records = [record for record in records if Path(record.kb_path).parent.as_posix() == path or Path(record.kb_path).parent.as_posix().startswith(f"{path}/")]
            folders.append(
                {
                    "path": path,
                    "type": schema["effective_schema"].get("type"),
                    "scope_id": schema["effective_schema"].get("scope_id"),
                    "criticality": schema["effective_schema"].get("criticality"),
                    "document_count": len(nested_records),
                    "direct_document_count": len(direct_records),
                    "has_index": (self.config.context_repo / path / "index.md").is_file(),
                    "has_log": (self.config.context_repo / path / "log.md").is_file(),
                }
                | self._supporting_sources_payload(schema["effective_schema"])
            )
        return folders

    def read_context_index(self, folder: str | None = None, scope_id: str | None = None) -> dict:
        entry = self.repository.content.read_okf_index(folder)
        entry.update(self._folder_supporting_sources_payload(folder))
        entry["entries"] = self.list_context_documents(type="", scope_id=scope_id, folder=folder, limit=100)
        return entry

    def read_context_log(self, folder: str | None = None, scope_id: str | None = None) -> dict:
        entry = self.repository.content.read_okf_log(folder)
        entry.update(self._folder_supporting_sources_payload(folder))
        entry["git_history"] = self.repository.content.git.history(folder, limit=10)
        return entry

    def list_context_documents(
        self,
        type: str,
        scope_id: str | None = None,
        folder: str | None = None,
        limit: int = 100,
    ) -> list[dict]:
        records = [
            record
            for record in self.repository.runtime_records(include_body=False)
            if record.status == "approved"
            and self.repository._is_current(record)
            and (not type or record.type == type)
            and self._record_visible_for_scope(record, scope_id)
            and self._record_in_folder(record, folder)
        ]
        return [self._record_summary(record) for record in records[: max(limit, 0)]]

    def read_context_document(self, path: str, scope_id: str | None = None) -> dict:
        records = [
            record
            for record in self.repository.runtime_records(include_body=True)
            if record.kb_path == path and record.status == "approved" and self.repository._is_current(record)
        ]
        if not records:
            raise FileNotFoundError(path)
        record = records[0]
        if not self._record_visible_for_scope(record, scope_id):
            raise PermissionError("document is not visible for the requested scope")
        entry = self.repository.content.read_okf_entry(path)
        entry.update(self._supporting_sources_payload(record))
        return entry

    def search_collection(self, collection: str, query: str, limit: int = 10) -> list[dict]:
        results = self.collections.search([collection], query, top_k=limit)
        flattened = []
        for item in results:
            citation = item["citation"]
            flattened.append(
                {
                    "collection_id": citation["collection_id"],
                    "source_id": citation["source_document_id"],
                    "source_title": citation["source_title"],
                    "source_path": citation["source_path"],
                    "location": citation["location"],
                    "unit_id": citation["unit_id"],
                    "snippet": item["text"],
                    "content_hash": citation["content_hash"],
                    "score": item["score"],
                }
            )
        return flattened

    def read_collection_source(self, collection: str, source_id: str) -> dict:
        return self.collections.read_source(collection, source_id)

    def validate_context(self) -> dict:
        return self.repository.content.validation_report()

    def scan_okf_folder(self, source_folder: str | Path) -> dict:
        return self.importer.scan(source_folder)

    def import_okf_folder(self, source_folder: str | Path, author: str) -> dict:
        plan = self.importer.scan(source_folder)
        return self.importer.apply(plan, author)

    def scan_uploaded_okf_folder(self, folder_name: str, files: list[dict]) -> dict:
        return self.importer.scan_uploaded(folder_name, files)

    def import_uploaded_okf_folder(self, folder_name: str, files: list[dict], author: str) -> dict:
        return self.importer.apply_uploaded(folder_name, files, author)

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

    def _record_summary(self, record) -> dict:
        summary = {
            "title": record.title,
            "path": record.kb_path,
            "type": record.type,
            "scope_id": record.scope_id,
            "status": record.status,
            "criticality": record.criticality,
            "description": record.okf.get("description", ""),
            "content_hash": record.content_hash,
            "links": record.links,
            "external_links": record.external_links,
            "citations": record.citations,
            "headings": record.headings,
        }
        if record.criticality != "controlled":
            summary["supporting_sources"] = record.supporting_sources
        return summary

    def _record_visible_for_scope(self, record, scope_id: str | None) -> bool:
        if not scope_id:
            return True
        if not record.scope_id:
            return True
        try:
            return record.scope_id in self.repository.content.scope_ancestors(scope_id)
        except ValueError:
            return False

    @staticmethod
    def _record_in_folder(record, folder: str | None) -> bool:
        if not folder:
            return True
        parent = Path(record.kb_path).parent.as_posix()
        return parent == folder or parent.startswith(f"{folder}/")

    def _folder_supporting_sources_payload(self, folder: str | None) -> dict:
        schema = self.repository.content.read_schema(folder or "")
        return self._supporting_sources_payload(schema["effective_schema"])

    @staticmethod
    def _supporting_sources_payload(metadata) -> dict:
        criticality = metadata.get("criticality") if isinstance(metadata, dict) else metadata.criticality
        if criticality == "controlled":
            return {}
        supporting_sources = metadata.get("supporting_sources", {}) if isinstance(metadata, dict) else metadata.supporting_sources
        return {"supporting_sources": supporting_sources}
